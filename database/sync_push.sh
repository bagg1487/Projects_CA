#!/usr/bin/env bash
###############################################################################
# sync_push.sh — Экспорт БД → Git commit → Git push
#
# Использование:
#   cd database/
#   ./sync_push.sh ["Коммит-сообщение"]
#
# Что делает:
#   1. Проверяет что Docker-контейнер запущен
#   2. Делает pg_dump базы parts_catalog в full_backup.sql
#   3. Коммитит изменения в Git
#   4. Пушит в удалённый репозиторий (GitHub)
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
NC='\033[0m' # No Color

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# ---------- 1. Проверка Docker ----------
log_info "Проверка Docker-контейнера..."
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log_error "Контейнер '${CONTAINER_NAME}' не запущен!"
    log_info "Запусти: docker-compose up -d"
    exit 1
fi
log_info "Контейнер запущен ✓"

# ---------- 2. pg_dump ----------
log_info "Экспорт базы данных '${DB_NAME}'..."
docker exec -e PGPASSWORD="${DB_PASSWORD}" \
    "${CONTAINER_NAME}" \
    pg_dump -U "${DB_USER}" -d "${DB_NAME}" --no-owner --no-privileges \
    > "${GIT_ROOT}/database/${BACKUP_FILE}"

BACKUP_SIZE=$(du -h "${GIT_ROOT}/database/${BACKUP_FILE}" | cut -f1)
log_info "Дамп сохранён: ${BACKUP_SIZE} ✓"

# ---------- 3. Git commit ----------
cd "${GIT_ROOT}"

if ! git diff --quiet -- "database/${BACKUP_FILE}" 2>/dev/null; then
    COMMIT_MSG="${1:-sync: обновить дамп БД $(date '+%Y-%m-%d %H:%M')}"
    log_info "Git commit: ${COMMIT_MSG}"
    git add "database/${BACKUP_FILE}"
    git commit -m "${COMMIT_MSG}"
    log_info "Коммит создан ✓"
else
    log_warn "Изменений в БД не обнаружено — коммит пропущен"
fi

# ---------- 4. Git push ----------
log_info "Git push..."
if git remote -v | grep -q origin; then
    git push
    log_info "Push завершён ✓"
else
    log_warn "Нет настроенного remote 'origin' — push пропущен"
    log_info "Добавь remote: git remote add origin <URL>"
fi

log_info "═══════════════════════════════════════════"
log_info "  Синхронизация завершена успешно!"
log_info "═══════════════════════════════════════════"
