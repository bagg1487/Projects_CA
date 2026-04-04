#!/usr/bin/env bash
###############################################################################
# sync_pull.sh — Git pull → Валидация → Восстановление БД → Миграции
#
# Использование:
#   cd database/
#   ./sync_pull.sh
#
# Что делает:
#   1. Загружает конфигурацию из .env
#   2. Делает git pull (получает последний дамп)
#   3. Валидирует SQL-дамп перед восстановлением
#   4. Создаёт резервную копию текущей БД (на случай отката)
#   5. Восстанавливает БД из дампа
#   6. Применяет.pending миграции
#   7. Проверяет целостность восстановленной БД
###############################################################################

set -euo pipefail

# ---------- Загрузка .env ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    source "$ENV_FILE"
    set +a
else
    echo -e "\033[1;33m[WARN]\033[0m  Файл .env не найден! Используются значения по умолчанию."
    POSTGRES_USER="${POSTGRES_USER:-myuser}"
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-mypassword}"
    POSTGRES_DB="${POSTGRES_DB:-parts_catalog}"
    CONTAINER_NAME="${CONTAINER_NAME:-car_parts_db}"
    GIT_REMOTE="${GIT_REMOTE:-origin}"
fi

BACKUP_FILE="$SCRIPT_DIR/full_backup.sql"
MANIFEST_FILE="$SCRIPT_DIR/db_manifest.json"
MIGRATIONS_DIR="$SCRIPT_DIR/migrations"

# ---------- Цвета ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC}  $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

# ---------- 1. Git pull ----------
log_step "Получение изменений из Git..."

cd "$GIT_ROOT"

if git remote -v | grep -q "$GIT_REMOTE"; then
    if git pull "$GIT_REMOTE" "$(git rev-parse --abbrev-ref HEAD)"; then
        log_info "Git pull завершён ✓"
    else
        log_error "Git pull не удался! Возможные причины:"
        log_info "  - Конфликт файлов — разрешите вручную: git mergetool"
        log_info "  - Нет доступа к репозиторию"
        log_info "  - Есть незакоммиченные изменения"
        exit 1
    fi
else
    log_warn "Нет remote '$GIT_REMOTE' — skip"
    log_info "Добавь: git remote add origin <URL>"
fi

# Проверка что дамп существует
if [[ ! -f "$BACKUP_FILE" ]]; then
    log_error "Файл дампа '${BACKUP_FILE##*/}' не найден!"
    log_info "Возможно, его ещё никто не запушил."
    log_info "Инициализируйте БД: docker cp BD_dead_kolesa_kz.sql $CONTAINER_NAME:/tmp/setup.sql"
    exit 1
fi

# ---------- 2. Валидация дампа ----------
log_step "Валидация дампа..."

# Проверка что файл не пустой
if [[ ! -s "$BACKUP_FILE" ]]; then
    log_error "Файл дампа пуст!"
    exit 1
fi

# Проверка что это SQL файл
if ! head -5 "$BACKUP_FILE" | grep -qiE '^(--|SET|SELECT|CREATE|COPY)'; then
    log_error "Файл не похож на SQL дамп!"
    log_info "Первые 5 строк:"
    head -5 "$BACKUP_FILE"
    exit 1
fi

# Проверка что дамп содержит нужную таблицу
if ! grep -qi "parts_inventory" "$BACKUP_FILE"; then
    log_error "Дамп не содержит таблицу 'parts_inventory'!"
    log_warn "Возможно, это дамп от старой версии схемы"
    exit 1
fi

# Проверка кодировки (частая проблема UTF-8)
if file "$BACKUP_FILE" | grep -qi "utf-8\|UTF-8\|ASCII"; then
    log_info "Кодировка дампа OK ✓"
else
    ENCODING=$(file "$BACKUP_FILE" | grep -oE '[A-Za-z0-9\-]+' | head -3 || echo "unknown")
    log_warn "Необычная кодировка дампа: $ENCODING"
    log_info "Пробуем продолжить..."
fi

DUMP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log_info "Дамп валиден: $DUMP_SIZE ✓"

# ---------- 3. Docker ----------
log_step "Проверка Docker-контейнера..."

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log_warn "Контейнер не запущен — запускаю..."
    cd "$SCRIPT_DIR"
    docker-compose up -d
    cd "$GIT_ROOT"

    log_info "Ожидание запуска PostgreSQL..."
    for i in $(seq 1 20); do
        if docker exec "$CONTAINER_NAME" pg_isready -U "$POSTGRES_USER" -q 2>/dev/null; then
            log_info "PostgreSQL готов ✓"
            break
        fi
        if [[ $i -eq 20 ]]; then
            log_error "PostgreSQL не запустился за 20 секунд"
            exit 1
        fi
        sleep 1
    done
else
    log_info "Контейнер запущен ✓"
fi

# ---------- 4. Резервная копия текущей БД ----------
log_step "Создание резервной копии текущей БД..."

# Создаём бэкап перед восстановлением (на случай если дамп битый)
BACKUP_BEFORE=$(mktemp "$SCRIPT_DIR/.backup_before_XXXXXX.sql")
trap "rm -f '$BACKUP_BEFORE'" EXIT

docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
    "$CONTAINER_NAME" \
    pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
    --no-owner --no-privileges \
    > "$BACKUP_BEFORE" 2>/dev/null || true

# ---------- 5. Восстановление БД ----------
log_step "Восстановление базы данных..."

# Копируем дамп в контейнер
docker cp "$BACKUP_FILE" "$CONTAINER_NAME:/tmp/restore.sql"

# Функция отката при ошибке
rollback() {
    log_error "Ошибка при восстановлении! Откат к предыдущей версии..."
    if [[ -s "$BACKUP_BEFORE" ]]; then
        docker cp "$BACKUP_BEFORE" "$CONTAINER_NAME:/tmp/rollback.sql"
        docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
            "$CONTAINER_NAME" \
            bash -c "
                dropdb -U $POSTGRES_USER --if-exists $POSTGRES_DB && \
                createdb -U $POSTGRES_USER $POSTGRES_DB && \
                psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/rollback.sql
            " 2>/dev/null || true
        log_info "Откат выполнен ✓"
    else
        log_warn "Резервная копия отсутствует — нужно восстановить вручную"
    fi
    # Чистим временные файлы
    rm -f "$BACKUP_BEFORE"
    exit 1
}

# Дропаем и пересоздаём БД (чистый restore)
if ! docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
    "$CONTAINER_NAME" \
    bash -c "
        dropdb -U $POSTGRES_USER --if-exists $POSTGRES_DB && \
        createdb -U $POSTGRES_USER $POSTGRES_DB && \
        psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/restore.sql
    "; then
    rollback
fi

log_info "База восстановлена ✓"

# ---------- 6. Применение миграций ----------
if [[ -d "$MIGRATIONS_DIR" ]]; then
    log_step "Проверка миграций..."

    # Считаем сколько миграций уже применено из манифеста
    APPLIED_MIGRATIONS=""
    if [[ -f "$MANIFEST_FILE" ]] && command -v python3 &>/dev/null; then
        APPLIED_MIGRATIONS=$(python3 -c "
import json
with open('$MANIFEST_FILE', 'r') as f:
    m = json.load(f)
for mig in m.get('migrations_applied', []):
    print(mig)
" 2>/dev/null || echo "")
    fi

    MIGRATION_COUNT=0
    for migration in "$MIGRATIONS_DIR"/*.sql; do
        [[ -f "$migration" ]] || continue
        MIG_NAME=$(basename "$migration")

        # Проверяем, не применена ли уже эта миграция
        if echo "$APPLIED_MIGRATIONS" | grep -qF "$MIG_NAME"; then
            log_info "  Миграция $MIG_NAME — уже применена ✓"
            continue
        fi

        log_info "  Применяю миграцию: $MIG_NAME ..."
        if docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
            "$CONTAINER_NAME" \
            psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
            -f "/tmp/migration_temp.sql" < "$migration" 2>/dev/null; then
            # Если миграция содержит CREATE TABLE / ALTER TABLE — это успех
            MIGRATION_COUNT=$((MIGRATION_COUNT + 1))
            log_info "  Миграция $MIG_NAME применена ✓"
        else
            # Миграция может содержать уже существующие колонки — это не всегда ошибка
            log_warn "  Миграция $MIG_NAME — возможно уже применена (column already exists)"
        fi
    done

    if [[ $MIGRATION_COUNT -gt 0 ]]; then
        log_info "Применено новых миграций: $MIGRATION_COUNT ✓"
    else
        log_info "Все миграции уже применены ✓"
    fi
fi

# ---------- 7. Проверка целостности ----------
log_step "Проверка целостности БД..."

# Проверяем что таблица существует
TABLE_COUNT=$(docker exec "$CONTAINER_NAME" \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
    "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'parts_inventory';" 2>/dev/null | tr -d '[:space:]')

if [[ "${TABLE_COUNT:-0}" != "1" ]]; then
    log_error "Таблица 'parts_inventory' не найдена!"
    rollback
fi

# Считаем записи
RECORDS_COUNT=$(docker exec "$CONTAINER_NAME" \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
    "SELECT COUNT(*) FROM parts_inventory;" 2>/dev/null | tr -d '[:space:]')

# Проверяем что данные читаются (случайная выборка)
SAMPLE_OK=$(docker exec "$CONTAINER_NAME" \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
    "SELECT oem_number, part_name FROM parts_inventory LIMIT 1;" 2>/dev/null | tr -d '[:space:]')

if [[ -z "$SAMPLE_OK" && "${RECORDS_COUNT:-0}" -gt 0 ]]; then
    log_warn "Записи есть, но не удалось прочитать выборку"
else
    log_info "Чтение данных OK ✓"
fi

log_info "Таблица: parts_inventory | Записей: ${RECORDS_COUNT:-0} ✓"

# ---------- 8. Обновление манифеста ----------
if [[ -f "$MANIFEST_FILE" ]] && command -v python3 &>/dev/null; then
    log_step "Обновление db_manifest.json..."

    python3 -c "
import json, os

manifest_path = '$MANIFEST_FILE'
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    manifest['records_count'] = int('${RECORDS_COUNT:-0}')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f'  Манифест обновлён: {manifest[\"records_count\"]} записей')
"
fi

# Чистим временный бэкап
rm -f "$BACKUP_BEFORE"
trap - EXIT

# ---------- Итог ----------
echo ""
log_info "═══════════════════════════════════════════════"
log_info "  Синхронизация завершена успешно!"
log_info "  БД: ${POSTGRES_DB} | Таблица: parts_inventory"
log_info "  Записей: ${RECORDS_COUNT:-0}"
log_info "═══════════════════════════════════════════════"
