#!/usr/bin/env bash
###############################################################################
# apply_migrations.sh — Применить только миграции БЕЗ потери данных
#
# Использование:
#   cd database/
#   ./apply_migrations.sh
#
# Когда использовать:
#   - Кто-то добавил новую миграцию (ALTER TABLE, новая колонка)
#   - Вы сделали git pull и получили новый .sql файл в migrations/
#   - НЕ нужно пересоздавать всю БД — только применить изменения схемы
#   - Данные в БД должны сохраниться
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
    echo -e "\033[1;33m[WARN]\033[0m  .env не найден, использую значения по умолчанию"
    POSTGRES_USER="${POSTGRES_USER:-myuser}"
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-mypassword}"
    POSTGRES_DB="${POSTGRES_DB:-parts_catalog}"
    CONTAINER_NAME="${CONTAINER_NAME:-car_parts_db}"
fi

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

# ---------- 1. Проверки ----------
log_step "Проверки..."

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    log_error "Контейнер '$CONTAINER_NAME' не запущен!"
    exit 1
fi

if ! docker exec "$CONTAINER_NAME" pg_isready -U "$POSTGRES_USER" -q 2>/dev/null; then
    log_error "PostgreSQL не отвечает!"
    exit 1
fi

if [[ ! -d "$MIGRATIONS_DIR" ]]; then
    log_error "Директория миграций '$MIGRATIONS_DIR' не найдена!"
    exit 1
fi

MIG_FILES=("$MIGRATIONS_DIR"/*.sql)
if [[ ! -f "${MIG_FILES[0]:-}" ]]; then
    log_info "Нет файлов миграций — применять нечего"
    exit 0
fi

log_info "Контейнер OK, миграции найдены ✓"

# ---------- 2. Получить список применённых миграций ----------
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

# ---------- 3. Применить миграции ----------
log_step "Применение миграций..."

APPLIED_COUNT=0
SKIPPED_COUNT=0
ERRORS=()

for migration in "${MIG_FILES[@]}"; do
    [[ -f "$migration" ]] || continue
    MIG_NAME=$(basename "$migration")

    # Проверяем, не применена ли уже
    if echo "$APPLIED_MIGRATIONS" | grep -qF "$MIG_NAME"; then
        log_info "  $MIG_NAME — уже применена ✓"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
        continue
    fi

    log_info "  Применяю: $MIG_NAME ..."

    # Копируем миграцию в контейнер
    docker cp "$migration" "$CONTAINER_NAME:/tmp/migration_apply.sql"

    # Пробуем применить
    if docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
        "$CONTAINER_NAME" \
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
        -v ON_ERROR_STOP=1 \
        -f /tmp/migration_apply.sql 2>&1; then

        APPLIED_COUNT=$((APPLIED_COUNT + 1))
        log_info "  $MIG_NAME — применена ✓"

        # Добавляем в манифест
        if [[ -f "$MANIFEST_FILE" ]] && command -v python3 &>/dev/null; then
            python3 -c "
import json
with open('$MANIFEST_FILE', 'r', encoding='utf-8') as f:
    m = json.load(f)
if '$MIG_NAME' not in m.get('migrations_applied', []):
    m.setdefault('migrations_applied', []).append('$MIG_NAME')
with open('$MANIFEST_FILE', 'w', encoding='utf-8') as f:
    json.dump(m, f, indent=2, ensure_ascii=False)
" 2>/dev/null
        fi
    else
        # Ошибка — возможно колонка уже существует
        log_warn "  $MIG_NAME — ошибка при применении (возможно уже существует)"
        ERRORS+=("$MIG_NAME")
    fi
done

# ---------- 4. Итог ----------
echo ""
log_info "═══════════════════════════════════════════════"
log_info "  Миграции завершены"
log_info "  Применено:  $APPLIED_COUNT"
log_info "  Пропущено:  $SKIPPED_COUNT"

if [[ ${#ERRORS[@]} -gt 0 ]]; then
    log_warn "  Ошибки: ${ERRORS[*]}"
    log_info "  Проверьте что миграции совместимы с вашей схемой"
fi

log_info "═══════════════════════════════════════════════"
