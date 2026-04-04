#!/usr/bin/env bash
###############################################################################
# sync_push.sh — Валидация → Export БД → Pull → Commit → Push
#
# Использование:
#   cd database/
#   ./sync_push.sh ["Коммит-сообщение"]
#
# Что делает:
#   1. Загружает конфигурацию из .env
#   2. Проверяет зависимости (Docker, Git, psycopg2)
#   3. Проверяет что контейнер запущен
#   4. Делает git pull (чтобы не перезаписать чужие изменения)
#   5. Создаёт дамп БД с валидацией
#   6. Обновляет db_manifest.json
#   7. Коммитит и пушит изменения
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
    echo -e "\033[1;33m[WARN]\033[0m  Скопируйте: cp database/.env.example database/.env"
    POSTGRES_USER="${POSTGRES_USER:-myuser}"
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-mypassword}"
    POSTGRES_DB="${POSTGRES_DB:-parts_catalog}"
    CONTAINER_NAME="${CONTAINER_NAME:-car_parts_db}"
    GIT_REMOTE="${GIT_REMOTE:-origin}"
fi

BACKUP_FILE="$SCRIPT_DIR/full_backup.sql"
MANIFEST_FILE="$SCRIPT_DIR/db_manifest.json"

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

# ---------- 1. Проверка зависимостей ----------
log_step "Проверка зависимостей..."

for cmd in docker git; do
    if ! command -v "$cmd" &>/dev/null; then
        log_error "'$cmd' не установлен!"
        exit 1
    fi
done

# Проверка что мы в git репозитории
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    log_error "Это не git репозиторий!"
    exit 1
fi

log_info "Зависимости OK ✓"

# ---------- 2. Проверка Docker ----------
log_step "Проверка контейнера '${CONTAINER_NAME}'..."

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log_error "Контейнер '${CONTAINER_NAME}' не запущен!"
    log_info "Запусти: cd database && docker-compose up -d"
    exit 1
fi

# Проверка что PostgreSQL отвечает
if ! docker exec "$CONTAINER_NAME" pg_isready -U "$POSTGRES_USER" -q 2>/dev/null; then
    log_error "PostgreSQL не отвечает внутри контейнера!"
    log_info "Подождите 10-15 секунд и попробуйте снова"
    exit 1
fi

log_info "Контейнер запущен и готов ✓"

# ---------- 3. Git pull (перед push!) ----------
log_step "Проверка обновлений с GitHub..."

if git remote -v | grep -q "$GIT_REMOTE"; then
    # Сохраняем текущий коммит
    BEFORE_COMMIT=$(git rev-parse HEAD)

    # Пытаемся получить обновления
    if git pull "$GIT_REMOTE" "$(git rev-parse --abbrev-ref HEAD)" --quiet 2>/dev/null; then
        AFTER_COMMIT=$(git rev-parse HEAD)
        if [[ "$BEFORE_COMMIT" != "$AFTER_COMMIT" ]]; then
            log_warn "Получены обновления с GitHub! Ваш локальный дамп может быть устаревшим."
            log_info "Рекомендуется сначала запустить: ./sync_pull.sh"

            # Спрашиваем подтверждение
            read -r -p "Продолжить и перезаписать удалённый дамп? (y/N): " confirm
            if [[ "$confirm" != "y" && "$confirm" != "Y" && "$confirm" != "д" && "$confirm" != "Д" ]]; then
                log_info "Отменено. Сначала выполните: ./sync_pull.sh"
                exit 0
            fi
        else
            log_info "Локальная версия актуальна ✓"
        fi
    else
        log_warn "Не удалось выполнить git pull (возможно, есть локальные изменения)"
        log_info "Продолжаем..."
    fi
else
    log_warn "Нет remote '$GIT_REMOTE' — проверка пропущена"
    log_info "Добавь: git remote add origin <URL>"
fi

# ---------- 4. Создание дампа ----------
log_step "Создание дампа базы данных '${POSTGRES_DB}'..."

# Временный файл для безопасного создания дампа
TEMP_DUMP=$(mktemp "$SCRIPT_DIR/.dump_XXXXXX.sql")
trap "rm -f '$TEMP_DUMP'" EXIT

docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
    "$CONTAINER_NAME" \
    pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
    --no-owner --no-privileges \
    --encoding=UTF8 \
    > "$TEMP_DUMP" 2>/dev/null

# Проверка что дамп не пустой
if [[ ! -s "$TEMP_DUMP" ]]; then
    log_error "Дамп пуст! Что-то пошло не так при экспорте."
    rm -f "$TEMP_DUMP"
    exit 1
fi

# Проверка что дамп содержит SQL (начинается с комментария или SET)
if ! head -5 "$TEMP_DUMP" | grep -qiE '^(--|SET|SELECT|CREATE)'; then
    log_error "Дамп не похож на SQL файл! Проверьте содержимое:"
    head -5 "$TEMP_DUMP"
    rm -f "$TEMP_DUMP"
    exit 1
fi

# Проверка что дамп содержит нашу таблицу
if ! grep -qi "parts_inventory" "$TEMP_DUMP"; then
    log_error "Дамп не содержит таблицу 'parts_inventory'!"
    log_warn "Возможно, подключились не к той базе данных"
    rm -f "$TEMP_DUMP"
    exit 1
fi

# Атомарная замена старого дампа
mv "$TEMP_DUMP" "$BACKUP_FILE"
# Отменяем trap, так как файл уже перемещён
trap - EXIT

DUMP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log_info "Дамп создан: $BACKUP_SIZE ✓"

# ---------- 5. Хэш дампа для manifest ----------
if command -v sha256sum &>/dev/null; then
    BACKUP_HASH=$(sha256sum "$BACKUP_FILE" | cut -d' ' -f1)
elif command -v shasum &>/dev/null; then
    BACKUP_HASH=$(shasum -a 256 "$BACKUP_FILE" | cut -d' ' -f1)
else
    BACKUP_HASH="none"
fi

# ---------- 6. Счётчик записей ----------
RECORDS_COUNT=$(docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
    "$CONTAINER_NAME" \
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
    "SELECT COUNT(*) FROM parts_inventory;" 2>/dev/null | tr -d '[:space:]')

# ---------- 7. Обновление db_manifest.json ----------
log_step "Обновление db_manifest.json..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    log_warn "Python не найден — manifest не обновлён"
    PYTHON=""
fi

if [[ -n "$PYTHON" ]]; then
    DEVICE_NAME="${COMPUTERNAME:-$(hostname 2>/dev/null || echo 'unknown')}"
    SYNC_TIME=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

    $PYTHON -c "
import json, os, sys

manifest_path = '$MANIFEST_FILE'
# Читаем существующий манифест или создаём новый
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
else:
    manifest = {
        'schema_version': 2,
        'description': 'Единая таблица parts_inventory',
        'migrations_applied': ['001_add_shop_url_column.sql']
    }

# Обновляем поля
manifest['last_sync'] = '$SYNC_TIME'
manifest['last_sync_device'] = '$DEVICE_NAME'
manifest['records_count'] = int('${RECORDS_COUNT}' or 0)
manifest['backup_hash'] = '$BACKUP_HASH'

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f'  Манифест обновлён: {manifest[\"records_count\"]} записей')
"
    log_info "db_manifest.json обновлён ✓"
fi

# ---------- 8. Git commit ----------
cd "$GIT_ROOT"

log_step "Git commit..."

# Проверяем есть ли изменения
if ! git diff --quiet -- "database/${BACKUP_FILE##*/}" "database/db_manifest.json" 2>/dev/null; then
    COMMIT_MSG="${1:-sync: обновить дамп БД $(date '+%Y-%m-%d %H:%M')}"
    git add "database/${BACKUP_FILE##*/}" "database/db_manifest.json"
    git commit -m "${COMMIT_MSG}"
    log_info "Коммит создан ✓"
else
    log_warn "Изменений в БД не обнаружено — коммит пропущен"
fi

# ---------- 9. Git push ----------
log_step "Git push..."

if git remote -v | grep -q "$GIT_REMOTE"; then
    if git push "$GIT_REMOTE" "$(git rev-parse --abbrev-ref HEAD)"; then
        log_info "Push завершён ✓"
    else
        log_error "Push не удался! Возможные причины:"
        log_info "  - Нет доступа к репозиторию"
        log_info "  - Есть обновления на remote — выполните git pull"
        exit 1
    fi
else
    log_warn "Нет remote '$GIT_REMOTE' — push пропущен"
    log_info "Добавь: git remote add origin <URL>"
fi

# ---------- Итог ----------
echo ""
log_info "═══════════════════════════════════════════════"
log_info "  Синхронизация завершена успешно!"
log_info "  Записей в БД: ${RECORDS_COUNT:-?}"
log_info "  Размер дампа: ${DUMP_SIZE}"
log_info "═══════════════════════════════════════════════"
