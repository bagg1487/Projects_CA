"""
Загрузчик данных из CSV/Excel в базу данных
Поддерживает различные форматы датасетов
"""

import pandas as pd
import psycopg2
from decimal import Decimal
import os
from typing import List, Dict
import random


def load_from_csv(file_path: str) -> List[Dict]:
    """
    Загружает данные из CSV файла
    
    Ожидаемые колонки: 
    - oem_number, part_name, brand, model, price, condition, quantity
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"Загружено {len(df)} записей из {file_path}")
        print(f"Колонки: {list(df.columns)}")
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка загрузки CSV: {e}")
        return []


def generate_sample_dataset(output_file='auto_parts_sample.csv'):
    """
    Генерирует реалистичный датасет запчастей
    (на случай, если нет готового CSV)
    """
    import random
    
    # Реальные данные
    parts_data = [
        # OEM, Название, Цена от, Цена до, Тип
        ('15208-AA100', 'Масляный фильтр', 500, 1500, 'Фильтр'),
        ('17801-0V010', 'Воздушный фильтр', 800, 2000, 'Фильтр'),
        ('04465-0W020', 'Тормозные колодки передние', 1500, 4000, 'Тормозная система'),
        ('04466-0W020', 'Тормозные колодки задние', 1200, 3500, 'Тормозная система'),
        ('48510-09L85', 'Амортизатор передний', 3000, 8000, 'Подвеска'),
        ('48520-09L85', 'Амортизатор задний', 2800, 7500, 'Подвеска'),
        ('13568-09070', 'Ремень ГРМ', 1200, 3500, 'Двигатель'),
        ('22401-AA560', 'Свечи зажигания (4 шт)', 400, 1200, 'Двигатель'),
        ('90916-03089', 'Термостат', 800, 2500, 'Охлаждение'),
        ('28100-0W030', 'Стартер', 5000, 15000, 'Электрооборудование'),
        ('27060-0W070', 'Генератор', 7000, 20000, 'Электрооборудование'),
        ('16400-0W210', 'Радиатор', 4000, 12000, 'Охлаждение'),
        ('12305-AA020', 'Масляный поддон', 2000, 5000, 'Двигатель'),
        ('23300-0W010', 'Топливный фильтр', 600, 1500, 'Фильтр'),
        ('31210-0W010', 'Ступица передняя', 3500, 8000, 'Ходовая часть'),
    ]
    
    brands = ['Toyota', 'Honda', 'Nissan', 'Mitsubishi', 'Subaru', 'Mazda', 'Hyundai', 'Kia']
    models = {
        'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser 200', 'Highlander'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Fit'],
        'Nissan': ['X-Trail', 'Qashqai', 'Juke', 'Patrol', 'Teana'],
        'Mitsubishi': ['Lancer', 'Outlander', 'Pajero Sport', 'ASX', 'Pajero'],
        'Subaru': ['Impreza', 'Forester', 'Outback', 'Legacy', 'WRX'],
        'Mazda': ['3', '6', 'CX-5', 'CX-9', 'MX-5'],
        'Hyundai': ['Solaris', 'Santa Fe', 'Tucson', 'Elantra', 'Creta'],
        'Kia': ['Rio', 'Sportage', 'Sorento', 'Ceed', 'Optima'],
    }
    
    conditions = ['new', 'used']
    cities = [
        'Новокузнецк', 'Кемерово', 'Москва', 'Санкт-Петербург', 
        'Новосибирск', 'Екатеринбург', 'Казань', 'Красноярск'
    ]
    stores = [
        'АвтоМир', 'Автозапчасти24', 'Автодок', 'Exist', 
        'Авторазбор №1', 'ЗапчастиКузбасс', 'Автоопт', 'Дром Запчасти'
    ]
    
    data = []
    for i in range(100):  # Генерируем 200 записей
        oem, name, price_min, price_max, category = random.choice(parts_data)
        brand = random.choice(brands)
        model = random.choice(models[brand])
        
        # Генерируем уникальный OEM для разнообразия
        if random.random() > 0.7:
            oem = f"{oem.split('-')[0]}-{random.randint(10000, 99999)}"
        
        part_name = f"{name} {brand} {model}"
        price = random.randint(price_min, price_max)
        quantity = random.randint(1, 25)
        condition = random.choice(conditions)
        year_start = random.randint(1995, 2015)
        year_end = year_start + random.randint(5, 10)
        
        data.append({
            'oem_number': oem,
            'part_name': part_name[:255],
            'brand': brand,
            'model': model,
            'price': price,
            'quantity': quantity,
            'condition': condition,
            'year_start': year_start,
            'year_end': year_end,
            'address': f"г. {random.choice(cities)}, ул. {random.choice(['Курако', 'Кирова', 'Транспортная', 'Ленина'])}, {random.randint(1, 100)}",
            'store_name': random.choice(stores),
            'phone': f"+7-{random.randint(900, 999)}-{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
            'photo_url': None,
            'body_code': None
        })
    
    # Сохраняем в CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Сгенерирован файл {output_file} с {len(data)} записями")
    return data


def save_to_database(parts: List[Dict]):
    """Сохраняет данные в базу данных"""
    if not parts:
        print("Нет данных для сохранения")
        return
    
    conn = psycopg2.connect(
        dbname="parts_catalog",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    # Очищаем таблицу перед загрузкой (опционально)
    clear = input("Очистить таблицу перед загрузкой? (y/n): ").strip().lower()
    if clear == 'y':
        cur.execute("TRUNCATE parts_inventory RESTART IDENTITY CASCADE")
        print("Таблица очищена")
    
    inserted = 0
    errors = 0
    
    for part in parts:
        try:
            cur.execute("""
                INSERT INTO parts_inventory (
                    oem_number, part_name, photo_url,
                    brand, model, body_code, year_start, year_end,
                    address, store_name, phone,
                    quantity, price, condition, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (
                part.get('oem_number', 'Не указан')[:50],
                part.get('part_name', 'Деталь')[:255],
                part.get('photo_url'),
                part.get('brand'),
                part.get('model'),
                part.get('body_code'),
                part.get('year_start'),
                part.get('year_end'),
                part.get('address'),
                part.get('store_name'),
                part.get('phone'),
                part.get('quantity', 1),
                Decimal(str(part.get('price', 0))),
                part.get('condition', 'used')
            ))
            inserted += 1
            
            if inserted % 50 == 0:
                print(f"  Загружено {inserted} записей...")
                
        except Exception as e:
            errors += 1
            print(f"Ошибка вставки: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"Загружено в БД: {inserted} запчастей")
    print(f"Ошибок: {errors}")
    print(f"{'='*50}")


def main():
    """Основная функция"""
    print("="*50)
    print("ЗАГРУЗЧИК ДАННЫХ В БАЗУ ЗАПЧАСТЕЙ")
    print("="*50)
    
    # Проверяем, существует ли CSV файл
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        print("\nНайдены CSV файлы:")
        for i, f in enumerate(csv_files, 1):
            print(f"  {i}. {f}")
        print(f"  {len(csv_files)+1}. Сгенерировать новый датасет")
        
        choice = input("\nВыберите файл (номер): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(csv_files):
            file_path = csv_files[int(choice)-1]
            print(f"\nЗагрузка из {file_path}...")
            data = load_from_csv(file_path)
        else:
            print("\nГенерация нового датасета...")
            data = generate_sample_dataset()
    else:
        print("\nCSV файлы не найдены. Генерируем новый датасет...")
        data = generate_sample_dataset()
    
    if not data:
        print("Не удалось получить данные")
        return
    
    print(f"\nПолучено {len(data)} записей")
    print("\nПример данных:")
    for i, item in enumerate(data[:3]):
        print(f"  {i+1}. {item.get('part_name', 'Нет названия')[:50]} - {item.get('price', 0)}₽")
    
    save = input("\nЗагрузить в базу данных? (y/n): ").strip().lower()
    if save == 'y':
        save_to_database(data)
    else:
        print("Данные не загружены")


if __name__ == "__main__":
    main()