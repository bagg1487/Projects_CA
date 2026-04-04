# 🗄️ База данных — Projects_CA

Система складского учёта автозапчастей. PostgreSQL 15+ в Docker.

---

## Структура БД

Единая таблица `parts_inventory` — всё в одном месте: запчасти, совместимость с авто, магазины, наличие и цены.

```
parts_inventory
├── oem_number, part_name, photo_url    # Запчасть
├── brand, model, body_code             # Совместимость
├── year_start, year_end
├── address, store_name, phone          # Магазин
├── shop_url
├── quantity, price, condition           # Наличие
└── updated_at
```

---

## 🚀 Запуск

### 1. Запустить контейнер

```bash
cd database/
docker-compose up -d
```

### 2. Создать таблицу (первый раз)

```bash
docker cp BD_dead_kolesa_kz.sql car_parts_db:/tmp/setup.sql
docker exec -it car_parts_db psql -U myuser -d parts_catalog -f /tmp/setup.sql
```

### 3. Проверить

```bash
docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "\dt"
```

---

## 🔄 Синхронизация между устройствами

Команда из 4 человек работает через GitHub. Один делает изменения → остальные получают.

### Отправить изменения (тот, кто внёс изменения)

```bash
cd database/
./sync_push.sh "описание что изменил"
```

### Получить изменения (все остальные)

```bash
cd database/
./sync_pull.sh
```

### Проверить состояние

```bash
./sync_status.sh
```

### Только применить миграции (без потери данных)

```bash
./apply_migrations.sh
```

> ⚠️ **Правило:** только один человек меняет БД за раз. Остальные получают через `sync_pull.sh`.

Подробности: [SYNC_README.md](SYNC_README.md)

---

## 🧪 Тесты

```bash
cd database/
python test.py
```

Проверяет: сортировку (Mergesort), дерево поиска (ОПД А2), подключение к БД, вывод данных.

---

## 📂 Файлы

| Файл | Что делает |
|------|-----------|
| `docker-compose.yml` | Запуск PostgreSQL в Docker |
| `BD_dead_kolesa_kz.sql` | Схема БД (создание таблицы) |
| `full_backup.sql` | Дамп БД для синхронизации |
| `test_bd.py` | CLI-приложение (меню: просмотр, поиск, сортировка, CRUD) |
| `test.py` | Набор тестов (18 штук) |
| `dataset.py` | Загрузчик данных из CSV |
| `sync_push.sh` / `sync_pull.sh` | Синхронизация через Git |
| `sync_status.sh` | Проверка статуса БД и Git |
| `apply_migrations.sh` | Применение миграций схемы |
| `migrations/` | SQL-файлы изменений схемы |

---

## 🔧 Вход в БД

```bash
docker exec -it car_parts_db psql -U myuser -d parts_catalog
```
