-- 1. Справочник марок и моделей (Теперь с числовыми годами для фильтрации)
CREATE TABLE car_models (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year_start INTEGER, -- Можно искать: WHERE year_start <= 2006
    year_end INTEGER,   -- И: WHERE year_end >= 2006
    body_code VARCHAR(20), -- Например, "RD1" для Honda CR-V
    UNIQUE(brand, model, body_code)
);

-- 2. Справочник адресов (без изменений)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL,
    store_name VARCHAR(100),
    phone VARCHAR(20)
);

-- 3. Таблица самих запчастей (Универсальное описание)
CREATE TABLE parts (
    id SERIAL PRIMARY KEY,
    oem_number VARCHAR(50) NOT NULL,
    part_name VARCHAR(255) NOT NULL,
    -- Убрали привязку к авто отсюда, так как одна деталь может быть для многих авто
    photo_url TEXT
);

-- 4. НОВАЯ ТАБЛИЦА: Совместимость (Связывает деталь с кузовами/моделями)
-- Именно здесь мы говорим: "Эта дверь подходит всем Honda CR-V RD1"
CREATE TABLE part_compatibility (
    part_id INTEGER REFERENCES parts(id) ON DELETE CASCADE,
    model_id INTEGER REFERENCES car_models(id) ON DELETE CASCADE,
    PRIMARY KEY (part_id, model_id)
);

-- 5. Таблица наличия и цен (Добавили проверку регистра для состояния)
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    part_id INTEGER NOT NULL REFERENCES parts(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL,
    -- Доработка: проверка регистра на уровне базы
    condition VARCHAR(10) NOT NULL CHECK (UPPER(condition) IN ('NEW', 'USED')),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для скорости
CREATE INDEX idx_oem ON parts(oem_number);
CREATE INDEX idx_model_years ON car_models(year_start, year_end);