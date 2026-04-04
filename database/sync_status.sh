#!/usr/bin/env bash
###############################################################################
# sync_status.sh — Показать статус синхронизации БД
#
# Использование:
#   cd database/
#   ./sync_status.sh
#
# Показывает:
#   - Версию схемы из манифеста
#   - Количество записей в локальной БД
#   - Когда была последняя синхронизация
#   - Какие миграции применены / ожидают применения
#   - Статус контейнера
#   - Есть ли локальные изменения не отправленные в Git
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
    POSTGRES_USER="${POSTGRES_USER:-myuser}"
    POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-mypassword}"
    POSTGRES_DB="${POSTGRES_DB:-parts_catalog}"
    CONTAINER_NAME="${CONTAINER_NAME:-car_parts_db}"
    GIT_REMOTE="${GIT_REMOTE:-origin}"
fi

MANIFEST_FILE="$SCRIPT_DIR/db_manifest.json"
MIGRATIONS_DIR="$SCRIPT_DIR/migrations"
BACKUP_FILE="$SCRIPT_DIR/full_backup.sql"

# ---------- Цвета ----------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_header() { echo -e "\n${MAGENTA}═══ $1${NC}"; }
print_ok()     { echo -e "  ${GREEN}✓${NC} $1"; }
print_warn()   { echo -e "  ${YELLOW}!${NC} $1"; }
print_error()  { echo -e "  ${RED}✗${NC} $1"; }
print_info()   { echo -e "    $1"; }

echo -e "\n${CYAN}╔══════════════════════════════════════════════╗"
echo -e "║     СТАТУС СИНХРОНИЗАЦИИ БД                 ║"
echo -e "╚══════════════════════════════════════════════╝${NC}"

# ---------- 1. Docker контейнер ----------
print_header "Контейнер"

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    print_ok "Контейнер '$CONTAINER_NAME' запущен"

    if docker exec "$CONTAINER_NAME" pg_isready -U "$POSTGRES_USER" -q 2>/dev/null; then
        print_ok "PostgreSQL отвечает"
    else
        print_warn "PostgreSQL не отвечает (возможно, запускается)"
    fi
else
    print_error "Контейнер '$CONTAINER_NAME' НЕ запущен"
    print_info "Запуск: cd database && docker-compose up -d"
fi

# ---------- 2. Манифест ----------
print_header "Манифест (db_manifest.json)"

if [[ -f "$MANIFEST_FILE" ]]; then
    print_ok "Файл манифеста найден"

    if command -v python3 &>/dev/null; then
        python3 -c "
import json, sys

with open('$MANIFEST_FILE', 'r', encoding='utf-8') as f:
    m = json.load(f)

schema = m.get('schema_version', '?')
desc = m.get('description', '')
last_sync = m.get('last_sync', None)
device = m.get('last_sync_device', '')
records = m.get('records_count', 0)
hash_val = m.get('backup_hash', '')

print(f'    Версия схемы:   {schema} — {desc}')
print(f'    Записей (посл.):  {records}')

if last_sync:
    print(f'    Посл. синхр.:   {last_sync}')
    print(f'    Устройство:     {device}')
else:
    print(f'    Посл. синхр.:   Не синхронизировано')
" 2>/dev/null || print_warn "Не удалось прочитать манифест"
    else
        print_warn "Python3 не найден — подробности недоступны"
        cat "$MANIFEST_FILE"
    fi
else
    print_warn "Манифест не найден (будет создан при первой синхронизации)"
fi

# ---------- 3. Локальная БД ----------
print_header "Локальная база данных"

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    # Записей
    RECORDS=$(docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
        "$CONTAINER_NAME" \
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
        "SELECT COUNT(*) FROM parts_inventory;" 2>/dev/null | tr -d '[:space:]' || echo "0")

    if [[ -n "$RECORDS" ]]; then
        print_ok "Записей в parts_inventory: $RECORDS"
    else
        print_error "Не удалось получить количество записей"
    fi

    # Таблица существует?
    TABLE_EXISTS=$(docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
        "$CONTAINER_NAME" \
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
        "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name='parts_inventory';" 2>/dev/null | tr -d '[:space:]' || echo "0")

    if [[ "${TABLE_EXISTS:-0}" == "1" ]]; then
        print_ok "Таблица 'parts_inventory' существует"

        # Колонки
        COL_COUNT=$(docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" \
            "$CONTAINER_NAME" \
            psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -t -c \
            "SELECT count(*) FROM information_schema.columns WHERE table_name='parts_inventory';" 2>/dev/null | tr -d '[:space:]' || echo "?")

        print_info "Колонок в таблице: $COL_COUNT"
    else
        print_error "Таблица 'parts_inventory' НЕ существует!"
        print_info "Создайте: docker cp BD_dead_kolesa_kz.sql $CONTAINER_NAME:/tmp/setup.sql"
        print_info "Затем:    docker exec -it $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -f /tmp/setup.sql"
    fi
else
    print_warn "Контейнер не запущен — проверка БД пропущена"
fi

# ---------- 4. Дамп файл ----------
print_header "Файл дампа (full_backup.sql)"

if [[ -f "$BACKUP_FILE" ]]; then
    DUMP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    DUMP_DATE=$(stat -c '%y' "$BACKUP_FILE" 2>/dev/null | cut -d'.' -f1 || stat -f '%Sm' "$BACKUP_FILE" 2>/dev/null || echo "?")
    print_ok "Дамп найден: $DUMP_SIZE ($DUMP_DATE)"
else
    print_warn "Дамп не найден"
fi

# ---------- 5. Миграции ----------
print_header "Миграции"

if [[ -d "$MIGRATIONS_DIR" ]]; then
    MIG_FILES=("$MIGRATIONS_DIR"/*.sql)
    if [[ -f "${MIG_FILES[0]}" ]]; then
        TOTAL_MIGS=${#MIG_FILES[@]}
        print_info "Файлов миграций: $TOTAL_MIGS"

        # Применённые из манифеста
        if command -v python3 &>/dev/null && [[ -f "$MANIFEST_FILE" ]]; then
            python3 -c "
import json, os, glob

with open('$MANIFEST_FILE', 'r') as f:
    m = json.load(f)
applied = set(m.get('migrations_applied', []))

all_migs = sorted(glob.glob('$MIGRATIONS_DIR/*.sql'))
for mig in all_migs:
    name = os.path.basename(mig)
    if name in applied:
        print(f'    {GREEN}✓{NC} {name} (применена)')
    else:
        print(f'    {YELLOW}○{NC} {name} (ожидает)')

pending = [m for m in all_migs if os.path.basename(m) not in applied]
if not pending:
    print(f'  ${GREEN}Все миграции применены ✓${NC}')
else:
    print(f'  ${YELLOW}Ожидает применения: {len(pending)}${NC}')
" 2>/dev/null || print_warn "Не удалось проверить миграции"
        else
            for mig in "$MIGRATIONS_DIR"/*.sql; do
                [[ -f "$mig" ]] && print_info "  $(basename "$mig")"
            done
        fi
    else
        print_info "Нет файлов миграций"
    fi
else
    print_info "Директория migrations не существует"
fi

# ---------- 6. Git статус ----------
print_header "Git статус"

cd "$GIT_ROOT"

if git rev-parse --is-inside-work-tree &>/dev/null; then
    # Remote
    if git remote -v | grep -q "$GIT_REMOTE"; then
        REMOTE_URL=$(git remote get-url "$GIT_REMOTE" 2>/dev/null || echo "?")
        print_ok "Remote '$GIT_REMOTE': $REMOTE_URL"

        # Есть ли обновления на remote?
        if git fetch "$GIT_REMOTE" --dry-run 2>/dev/null; then
            # Сравниваем локальный и удалённый коммиты
            LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "")
            REMOTE=$(git rev-parse "$GIT_REMOTE/$(git rev-parse --abbrev-ref HEAD)" 2>/dev/null || echo "")

            if [[ -n "$LOCAL" && -n "$REMOTE" ]]; then
                if [[ "$LOCAL" == "$REMOTE" ]]; then
                    print_ok "Локальная версия синхронизирована с remote"
                else
                    # Проверяем направление
                    AHEAD=$(git rev-list --count "$REMOTE".."$LOCAL" 2>/dev/null || echo "0")
                    BEHIND=$(git rev-list --count "$LOCAL".."$REMOTE" 2>/dev/null || echo "0")

                    if [[ "$AHEAD" -gt 0 && "$BEHIND" -eq 0 ]]; then
                        print_warn "Есть $AHEAD локальных коммитов не отправленных на GitHub"
                        print_info "Выполните: ./sync_push.sh"
                    elif [[ "$BEHIND" -gt 0 && "$AHEAD" -eq 0 ]]; then
                        print_warn "Есть $BEHIND коммитов на GitHub которые не получены локально"
                        print_info "Выполните: ./sync_pull.sh"
                    elif [[ "$AHEAD" -gt 0 && "$BEHIND" -gt 0 ]]; then
                        print_error "Расхождение! $AHEAD локальных и $BEHIND удалённых коммитов"
                        print_info "Выполните: git pull --rebase, затем ./sync_push.sh"
                    fi
                fi
            fi
        else
            print_warn "Не удалось проверить remote (нет сети?)"
        fi
    else
        print_warn "Нет remote '$GIT_REMOTE'"
        print_info "Добавь: git remote add origin <URL>"
    fi

    # Локальные изменения
    if ! git diff --quiet -- "database/" 2>/dev/null; then
        print_warn "Есть локальные изменения в database/"
        CHANGED=$(git diff --name-only -- "database/" 2>/dev/null | head -5)
        while IFS= read -r file; do
            print_info "  ~ $file"
        done <<< "$CHANGED"
    fi
else
    print_error "Это не git репозиторий!"
fi

# ---------- Итог ----------
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════"
echo -e "  Команды:"
echo -e "  ./sync_push.sh   — отправить изменения"
echo -e "  ./sync_pull.sh   — получить изменения"
echo -e "  ./sync_status.sh — этот отчёт"
echo -e "═══════════════════════════════════════════════${NC}"
echo ""
