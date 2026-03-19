-- Единая таблица запчастей с наличием и совместимостью
CREATE TABLE parts_inventory (
    id SERIAL PRIMARY KEY,
    -- Информация о запчасти
    oem_number VARCHAR(50) NOT NULL,
    part_name VARCHAR(255) NOT NULL,
    photo_url TEXT,
    
    -- Информация об авто (совместимость)
    brand VARCHAR(50),
    model VARCHAR(100),
    body_code VARCHAR(20),
    year_start INTEGER,
    year_end INTEGER,
    
    -- Информация о месте наличия
    address TEXT,
    store_name VARCHAR(100),
    phone VARCHAR(20),
    
    -- Наличие и состояние
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
    price DECIMAL(10, 2) NOT NULL,
    condition VARCHAR(10) NOT NULL CHECK (UPPER(condition) IN ('NEW', 'USED')),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для быстрого поиска
CREATE INDEX idx_oem_number ON parts_inventory(oem_number);
CREATE INDEX idx_brand_model ON parts_inventory(brand, model);
CREATE INDEX idx_years ON parts_inventory(year_start, year_end);
CREATE INDEX idx_store ON parts_inventory(store_name);
