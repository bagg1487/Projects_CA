import psycopg2

def test_db_setup():
    config = {
        "dbname": "parts_catalog",
        "user": "myuser",
        "password": "mypassword",
        "host": "localhost",
        "port": "5432"
    }

    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()

        # 1. Добавляем тестовую модель авто
        cur.execute("""
            INSERT INTO car_models (brand, model, body_code, year_start, year_end) 
            VALUES ('Honda', 'CR-V', 'RD1', 1995, 2001) 
            ON CONFLICT (brand, model, body_code) DO UPDATE SET brand=EXCLUDED.brand
            RETURNING id;
        """)
        model_id = cur.fetchone()[0]

        # 2. Добавляем саму запчасть
        cur.execute("""
            INSERT INTO parts (oem_number, part_name) 
            VALUES ('51220-S04-003', 'Шаровая опора') 
            RETURNING id;
        """)
        part_id = cur.fetchone()[0]

        # 3. Связываем деталь с машиной (Compatibility)
        cur.execute("INSERT INTO part_compatibility (part_id, model_id) VALUES (%s, %s);", (part_id, model_id))

        conn.commit()
        print("✅ Успех! Тестовые данные внесены и связаны.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    test_db_setup()