# Projects_CA

# Отчёт 12.03.2026 - создание БД
# Структура и взаимодействие таблиц
База данных спроектирована по принципам 3-й нормальной формы (3NF). Данные разделены таким образом, чтобы исключить дублирование и обеспечить целостность при каскадных операциях.

## 1. Таблица car_models (Справочник автомобилей)
Это фундаментальный справочник. Мы не пишем марку машины в каждой запчасти, а ссылаемся на эту таблицу.

Столбцы: id, brand (марка), model (модель), year_start/year_end (период выпуска), body_code (код кузова, например, RD1).

Особенность: Поля brand, model и body_code образуют UNIQUE constraint. Это гарантирует, что у тебя не будет двух одинаковых "Honda CR-V RD1" в базе.

## 2. Таблица parts (Каталог запчастей)
Здесь хранится "паспорт" детали. Она отделена от цен и складов, так как описание детали неизменно, где бы она ни лежала.

Столбцы: id, oem_number (артикул производителя), part_name (название), photo_url.

Взаимодействие: Является "ядром". На её id ссылаются таблицы совместимости и инвентаря.

## 3. Таблица part_compatibility (Таблица связей)
Связующее звено между parts и car_models.

Тип связи: Many-to-Many (Многие-ко-Многим).

Зачем это нужно: Одна и та же деталь (например, масляный фильтр) может подходить к 20 разным моделям авто. Вместо создания 20 копий детали, мы создаем 20 легких записей-ссылок в этой таблице.

## 4. Таблица locations (Точки хранения)
Справочник складов или магазинов.

Столбцы: id, address, store_name, phone.

Взаимодействие: Позволяет приложению выводить не просто «в наличии», а «в наличии по адресу ул. Ленина, 5».

## 5. Таблица inventory (Учет и коммерция)
Самая динамичная таблица. Здесь хранятся данные, которые меняются чаще всего.

Столбцы: part_id (какая деталь), location_id (где лежит), quantity (сколько), price (почем), condition (состояние).

Логика связей: * Связана с parts через FOREIGN KEY. Если удалить деталь из каталога, информация о её наличии удалится автоматически (ON DELETE CASCADE).

Контролирует состояние через CHECK (UPPER(condition) IN ('NEW', 'USED')), что исключает ошибки ввода.

# Технологический стек
Database: PostgreSQL 15+

Environment: Docker & Docker Compose

Language: Python 3.x

Driver: psycopg2-binary

# Логика взаимодействия с Python
Работа приложения строится по транзакционной модели. Пример процесса добавления новой единицы товара:

Validation: Программа проверяет существование модели авто в car_models.

Normalization: Если модель найдена, используется её ID. Если нет — создается новая запись.

Data Integrity: При добавлении запчасти в inventory, база автоматически проверяет поле condition. Благодаря ограничению CHECK (UPPER(condition) IN ('NEW', 'USED')), исключается попадание некорректных статусов.

Optimization: Поиск по артикулу (OEM) ускорен с помощью B-Tree индекса idx_oem.

# Основные SQL запросы
Получение полного отчета о наличии (JOIN запрос)
Этот запрос собирает данные из всех таблиц в одну удобную таблицу для интерфейса приложения:

SQL
SELECT 
    p.part_name, 
    p.oem_number, 
    m.brand, 
    m.model, 
    i.price, 
    i.quantity, 
    l.address
FROM parts p
JOIN part_compatibility pc ON p.id = pc.part_id
JOIN car_models m ON pc.model_id = m.id
JOIN inventory i ON p.id = i.part_id
JOIN locations l ON i.location_id = l.id
WHERE i.quantity > 0;

# Развертывание (Quick Start) \ Запуск контейнера:

# Bash
### ДЛЯ АКТИВАЦИИ ПРОПИШИ В ТЕРМИНАЛЕ В ПАПКЕ С ФАЙЛОМ
### ВКЛЮЧИ ДОКЕР
### docker-compose up -d

## Создание таблиц (Активация кода)
## Скопируй файл прямо в контейнер:
## docker cp BD_dead_kolesa_kz.sql car_parts_db:/tmp/setup.sql

## Запусти его выполнение внутри:
### docker exec -it car_parts_db psql -U myuser -d parts_catalog -f /tmp/setup.sql
# ДЛЯ ПРОВЕРКИ ЧТО ВСЁ СОЗДАЛОСЬ УСПЕШНО: docker exec -it car_parts_db psql -U myuser -d parts_catalog -c "\dt"

## Общая команда для входа в БД через терминал:
### docker exec -it car_parts_db psql -U myuser -d parts_catalog

# ПЕРЕД КАЖДЫМ КОММИТОМ ДЕЛАТЬ ЭТО:

### docker exec -t car_parts_db pg_dump -U myuser parts_catalog > full_backup.sql

# ДЛЯ ЭТОГО
## Напарник: делает pg_dump в файл full_backup.sql и пушит его в Git.
## Ты: делаешь git pull. Твой файл full_backup.sql на компьютере обновился.
## Ты: теперь тебе нужно "накатить" (импортировать) этот файл в свой локальный Docker.
## Команда для тебя (обновление твоей базы):
## Bash
## docker exec -i car_parts_db psql -U myuser -d parts_catalog < full_backup.sql
