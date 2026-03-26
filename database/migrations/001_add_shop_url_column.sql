-- Миграция: Добавление колонки shop_url в таблицу parts_inventory
-- Дата: 2026-03-26
-- Описание: Добавлено поле для хранения ссылок на магазины

-- Шаг 1: Добавить новую колонку shop_url
-- Используем DEFAULT '' для существующих записей
ALTER TABLE parts_inventory
ADD COLUMN shop_url VARCHAR(500) NOT NULL DEFAULT '';

-- Шаг 2: Создать индекс для ускорения поиска по URL
CREATE INDEX idx_shop_url ON parts_inventory(shop_url);

-- Проверка: вывести структуру таблицы
\d parts_inventory

-- Пример обновления для конкретной записи (опционально):
-- UPDATE parts_inventory 
-- SET shop_url = 'https://example.com/part/12345' 
-- WHERE oem_number = '12345-S12-123';
