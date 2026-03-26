# Projects_CA

# Отчёт 26.03.2026 - Добавление поля shop_url

## Изменения в структуре базы данных

### Новая колонка: `shop_url`

Добавлено поле для хранения ссылок на магазины/страницы товаров.

| Параметр | Значение |
|----------|----------|
| **Имя поля** | `shop_url` |
| **Тип данных** | `VARCHAR(500)` |
| **Ограничения** | `NOT NULL DEFAULT ''` |
| **Индекс** | `idx_shop_url` (B-Tree) |

**Обоснование:**
- Позволяет хранить прямые ссылки на товары в интернет-магазинах
- Упрощает переход к источнику запчасти
- Максимальная длина 500 символов покрывает большинство URL

---

## Обновлённые файлы

### 1. База данных

| Файл | Изменения |
|------|-----------|
| `database/BD_dead_kolesa_kz.sql` | Добавлена колонка `shop_url`, создан индекс |
| `database/full_backup.sql` | Обновлена структура таблицы и COPY-запрос |
| `database/migrations/001_add_shop_url_column.sql` | **Новый файл** — миграция для существующих БД |

### 2. CLI-приложение (`database/test_bd.py`)

**Функция `add_part()`:**
```python
shop_url = input("Ссылка на магазин (оставьте пустым, если нет): ").strip() or ''
```

**Функция `edit_part()`:**
```python
new_shop_url = input(f"Ссылка на магазин [{part['shop_url'] or ''}]: ").strip() or part['shop_url']
```

**Функция `print_parts()`:**
```python
if p.get('shop_url'):
    print(f"  Ссылка: {p['shop_url']}")
```

### 3. GUI-приложение (`client/`)

**`database.py` — полностью переписан:**
- Убраны JOIN'ы для 5 таблиц (устаревшая структура)
- Все запросы к единой таблице `parts_inventory`
- Новые методы: `add_part()`, `update_part()`, `delete_part()`, `get_all_brands()`, `get_all_locations()`

**`main.py` — обновлён:**
- Таблица инвентаря: добавлена колонка "Ссылка" (10 колонок вместо 9)
- Таблица каталога: добавлена колонка "Ссылка" (7 колонок вместо 6)
- Диалог `PartDialog`: поле `shopUrlEdit` для ввода URL
- Подключение к БД с паролем `mypassword`

---

## Применение миграции

### Для существующей БД:

```bash
# Способ 1: Через файл миграции
docker exec -i car_parts_db psql -U myuser -d parts_catalog < database/migrations/001_add_shop_url_column.sql

# Способ 2: Вручную через psql
docker exec -it car_parts_db psql -U myuser -d parts_catalog
```

```sql
-- Выполнить в psql:
ALTER TABLE parts_inventory ADD COLUMN shop_url VARCHAR(500) NOT NULL DEFAULT '';
CREATE INDEX idx_shop_url ON parts_inventory(shop_url);
```

### Проверка:

```bash
# Просмотр структуры таблицы
docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "\d parts_inventory"

# Проверка данных
docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "SELECT id, oem_number, shop_url FROM parts_inventory;"

# Проверка индекса
docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "\di idx_shop_url"
```

---

## Синхронизация с командой (Git workflow)

### Перед коммитом (экспорт БД):

```bash
# 1. Экспорт актуального состояния БД
docker exec -t car_parts_db pg_dump -U myuser parts_catalog > database/full_backup.sql

# 2. Добавление изменений
git add .

# 3. Коммит
git commit -m "Добавлено поле shop_url для ссылок на магазины"

# 4. Отправка на сервер
git push
```

### После pull (импорт обновлений):

```bash
# 1. Получить обновления
git pull

# 2. Применить миграцию (если есть новые файлы в database/migrations/)
docker exec -i car_parts_db psql -U myuser -d parts_catalog < database/migrations/001_add_shop_url_column.sql

# 3. Или импортировать полный дамп
docker exec -i car_parts_db psql -U myuser -d parts_catalog < database/full_backup.sql
```

---

## Технологический стек (актуально)

| Компонент | Версия |
|-----------|--------|
| PostgreSQL | 15+ |
| Python | 3.x |
| psycopg2-binary | 2.9.11 |
| PyQt6 | 6.10.2 |
| Docker | latest |
| Docker Compose | 3.8 |

---

## Структура таблицы `parts_inventory` (актуальная)

```
Column       | Type              | Nullable | Default
-------------+-------------------+----------+------------------
id           | integer           | NO       | nextval(...)
oem_number   | varchar(50)       | NO       | -
part_name    | varchar(255)      | NO       | -
photo_url    | text              | YES      | -
brand        | varchar(50)       | YES      | -
model        | varchar(100)      | YES      | -
body_code    | varchar(20)       | YES      | -
year_start   | integer           | YES      | -
year_end     | integer           | YES      | -
address      | text              | YES      | -
store_name   | varchar(100)      | YES      | -
phone        | varchar(20)       | YES      | -
shop_url     | varchar(500)      | NO       | ''  ← НОВОЕ
quantity     | integer           | YES      | 0
price        | numeric(10,2)     | NO       | -
condition    | varchar(10)       | NO       | -
updated_at   | timestamp         | YES      | now()
```

**Индексы:**
- `idx_oem_number` — поиск по OEM-артикулу
- `idx_brand_model` — поиск по марке/модели
- `idx_years` — фильтрация по годам
- `idx_store` — поиск по магазину
- `idx_shop_url` — **новый** поиск по URL

---

## Известные проблемы

1. **GUI требует доработки:**
   - Диалог редактирования не загружает существующие данные
   - Удаление по ID требует скрытой колонки в таблице

2. **Безопасность:**
   - Пароль БД хранится в открытом виде (`mypassword`)
   - Рекомендуется использовать `.env` файл

---

## Примечания

- Перед запуском CLI/GUI убедитесь, что миграция применена
- Пустые значения `shop_url` хранятся как `''` (пустая строка)
- Для существующих записей поле заполняется автоматически значением по умолчанию
