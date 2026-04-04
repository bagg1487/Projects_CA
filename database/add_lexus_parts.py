"""
Добавляет 10 записей запчастей для Lexus IS250 в базу данных
Запуск: python add_lexus_parts.py
"""

import psycopg2
from decimal import Decimal

# ---------- Настройки (из .env) ----------
DB_CONFIG = {
    "dbname": "parts_catalog",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432",
}

# ---------- Данные ----------
PARTS = [
    {
        "oem_number": "04465-53360",
        "part_name": "Тормозные колодки передние",
        "photo_url": "https://exist.ru/image/04465-53360.jpg",
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Москва, ул. Автозаводская, 23",
        "store_name": "АвтоМир",
        "phone": "+7 (495) 123-45-67",
        "shop_url": "https://exist.ru/art/04465-53360",
        "quantity": 12,
        "price": Decimal("3200.00"),
        "condition": "new",
    },
    {
        "oem_number": "04466-53070",
        "part_name": "Тормозные колодки задние",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Санкт-Петербург, пр. Невский, 100",
        "store_name": "Exist",
        "phone": "+7 (812) 987-65-43",
        "shop_url": "https://exist.ru/art/04466-53070",
        "quantity": 8,
        "price": Decimal("2800.00"),
        "condition": "new",
    },
    {
        "oem_number": "17801-31090",
        "part_name": "Воздушный фильтр двигателя",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Казань, ул. Декабристов, 45",
        "store_name": "Автодок",
        "phone": "+7 (843) 555-12-34",
        "shop_url": "",
        "quantity": 20,
        "price": Decimal("950.00"),
        "condition": "new",
    },
    {
        "oem_number": "90919-01253",
        "part_name": "Свечи зажигания (комплект 6 шт)",
        "photo_url": "https://exist.ru/image/90919-01253.jpg",
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Новосибирск, ул. Красный проспект, 78",
        "store_name": "Дром Запчасти",
        "phone": "+7 (383) 222-33-44",
        "shop_url": "https://exist.ru/art/90919-01253",
        "quantity": 5,
        "price": Decimal("1800.00"),
        "condition": "new",
    },
    {
        "oem_number": "48510-80435",
        "part_name": "Амортизатор передний левый",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Екатеринбург, ул. Ленина, 50",
        "store_name": "ЗапчастиКузбасс",
        "phone": "+7 (343) 777-88-99",
        "shop_url": "",
        "quantity": 3,
        "price": Decimal("6500.00"),
        "condition": "new",
    },
    {
        "oem_number": "48530-80615",
        "part_name": "Амортизатор задний правый",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Красноярск, пр. Мира, 12",
        "store_name": "Авторазбор №1",
        "phone": "+7 (391) 111-22-33",
        "shop_url": "https://avtorazbor.ru/lexus-is250",
        "quantity": 2,
        "price": Decimal("4200.00"),
        "condition": "used",
    },
    {
        "oem_number": "15600-31100",
        "part_name": "Масляный фильтр двигателя",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Москва, ул. Курако, 5",
        "store_name": "Автозапчасти24",
        "phone": "+7 (495) 333-44-55",
        "shop_url": "https://exist.ru/art/15600-31100",
        "quantity": 30,
        "price": Decimal("450.00"),
        "condition": "new",
    },
    {
        "oem_number": "90915-YZZD2",
        "part_name": "Фильтр масляный (оригинал Toyota)",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE30",
        "year_start": 2013,
        "year_end": 2020,
        "address": "г. Кемерово, ул. Советская, 33",
        "store_name": "Автоопт",
        "phone": "+7 (384) 444-55-66",
        "shop_url": "",
        "quantity": 15,
        "price": Decimal("520.00"),
        "condition": "new",
    },
    {
        "oem_number": "43512-53020",
        "part_name": "Тормозной диск передний",
        "photo_url": "https://exist.ru/image/43512-53020.jpg",
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE20",
        "year_start": 2005,
        "year_end": 2013,
        "address": "г. Москва, ул. Автозаводская, 23",
        "store_name": "АвтоМир",
        "phone": "+7 (495) 123-45-67",
        "shop_url": "https://exist.ru/art/43512-53020",
        "quantity": 4,
        "price": Decimal("5800.00"),
        "condition": "new",
    },
    {
        "oem_number": "17801-0P010",
        "part_name": "Воздушный фильтр (3 поколение XE30)",
        "photo_url": None,
        "brand": "Lexus",
        "model": "IS250",
        "body_code": "XE30",
        "year_start": 2013,
        "year_end": 2020,
        "address": "г. Санкт-Петербург, пр. Невский, 100",
        "store_name": "Exist",
        "phone": "+7 (812) 987-65-43",
        "shop_url": "https://exist.ru/art/17801-0P010",
        "quantity": 7,
        "price": Decimal("1100.00"),
        "condition": "new",
    },
]

# ---------- Скрипт ----------
def main():
    print("=" * 60)
    print("  Добавление запчастей Lexus IS250")
    print("=" * 60)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0
    errors = 0

    for i, part in enumerate(PARTS, 1):
        try:
            cur.execute("""
                INSERT INTO parts_inventory (
                    oem_number, part_name, photo_url,
                    brand, model, body_code, year_start, year_end,
                    address, store_name, phone, shop_url,
                    quantity, price, condition, updated_at
                ) VALUES (
                    %(oem_number)s, %(part_name)s, %(photo_url)s,
                    %(brand)s, %(model)s, %(body_code)s, %(year_start)s, %(year_end)s,
                    %(address)s, %(store_name)s, %(phone)s, %(shop_url)s,
                    %(quantity)s, %(price)s, %(condition)s, NOW()
                ) RETURNING id, oem_number, part_name
            """, part)

            result = cur.fetchone()
            conn.commit()
            inserted += 1
            print(f"  [{i:2d}/{len(PARTS)}] ✓ ID={result[0]} | {result[1]} — {result[2]}")

        except Exception as e:
            conn.rollback()
            errors += 1
            print(f"  [{i:2d}/{len(PARTS)}] ✗ Ошибка: {e}")

    cur.close()
    conn.close()

    print()
    print("=" * 60)
    print(f"  Готово! Добавлено: {inserted}, Ошибок: {errors}")
    print("=" * 60)


if __name__ == "__main__":
    main()
