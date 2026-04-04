#!/usr/bin/env bash
###############################################################################
# sync_pull.sh — Git pull → Восстановление БД из дампа
#
# Использование:
#   cd database/
#   ./sync_pull.sh
#
# Что делает:
#   1. Делает git pull (получает последний дамп с GitHub)
#   2. Запускает Docker-контейнер если не запущен
#   3. Восстанавливает БД из full_backup.sql
#   4. Проверяет что таблицы созданы
###############################################################################

set -euo pipefail

# ---------- Настройки ----------
DB_USER="myuser"
DB_PASSWORD="mypassword"
DB_NAME="parts_catalog"
CONTAINER_NAME="car_parts_db"
BACKUP_FILE="full_backup.sql"
GIT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ---------- Цвета для вывода ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

# ---------- 1. Git pull ----------
cd "${GIT_ROOT}"
log_step "Получение изменений из Git..."

if git remote -v | grep -q origin; then
    git pull
    log_info "Git pull завершён ✓"
else
    log_warn "Нет remote 'origin' — skip"
    log_info "Добавь: git remote add origin <URL>"
fi

# Проверка что дамп существует
if [[ ! -f "${GIT_ROOT}/database/${BACKUP_FILE}" ]]; then
    log_error "Файл дампа '${BACKUP_FILE}' не найден!"
    exit 1
fi

DUMP_DATE=$(stat -c %Y "${GIT_ROOT}/database/${BACKUP_FILE}" 2>/dev/null || stat -f %m "${GIT_ROOT}/database/${BACKUP_FILE}" 2>/dev/null)
DUMP_DATE_FMT=$(date -d "@${DUMP_DATE}" '+%Y-%m-%d %H:%M' 2>/dev/null || date -r "${DUMP_DATE}" '+%Y-%m-%d %H:%M' 2>/dev/null)
log_info "Дамп от: ${DUMP_DATE_FMT}"

# ---------- 2. Docker ----------
log_step "Проверка Docker-контейнера..."

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log_warn "Контейнер не запущен — запускаю..."
    cd "${GIT_ROOT}/database"
    docker-compose up -d
    # Ждём пока PostgreSQL стартанёт
    log_info "Ожидание запуска PostgreSQL..."
    for i in $(seq 1 15); do
        if docker exec "${CONTAINER_NAME}" pg_isready -U "${DB_USER}" -q 2>/dev/null; then
            log_info "PostgreSQL готов ✓"
            break
        fi
        if [[ $i -eq 15 ]]; then
            log_error "PostgreSQL не запустился за 15 секунд"
            exit 1
        fi
        sleep 1
    done
    cd "${GIT_ROOT}"
else
    log_info "Контейнер запущен ✓"
fi

# ---------- 3. Restore БД ----------
log_step "Восстановление базы данных..."

# Копируем дамп в контейнер
docker cp "${GIT_ROOT}/database/${BACKUP_FILE}" "${CONTAINER_NAME}:/tmp/restore.sql"

# Дропаем и пересоздаём БД (чистый restore)
docker exec -e PGPASSWORD="${DB_PASSWORD}" \
    "${CONTAINER_NAME}" \
    bash -c "
        dropdb -U ${DB_USER} --if-exists ${DB_NAME} && \
        createdb -U ${DB_USER} ${DB_NAME} && \
        psql -U ${DB_USER} -d ${DB_NAME} -f /tmp/restore.sql
    "

log_info "База восстановлена ✓"

# ---------- 4. Проверка ----------
log_step "Проверка таблиц..."
TABLE_COUNT=$(docker exec "${CONTAINER_NAME}" \
    psql -U "${DB_USER}" -d "${DB_NAME}" -t -c \
    "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")

TABLE_COUNT=$(echo "${TABLE_COUNT}" | tr -d '[:space:]')

if [[ "${TABLE_COUNT}" -gt 0 ]]; then
    log_info "Таблиц в БД: ${TABLE_COUNT} ✓"
else
    log_error "Таблицы не найдены! Проверь дамп."
    exit 1
fi

# ---------- 5. Итог ----------
log_info "═══════════════════════════════════════════"
log_info "  Синхронизация завершена успешно!"
log_info "  БД: ${DB_NAME} | Таблиц: ${TABLE_COUNT}"
log_info "═══════════════════════════════════════════"
