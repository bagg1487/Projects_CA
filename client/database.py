import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from decimal import Decimal
from typing import List, Optional, Dict, Any
from models import Part, InventoryItem


class Database:
    """Класс для работы с базой данных (backend)"""

    def __init__(self, dbname='parts_catalog', user='myuser',
                 password='mypassword', host='localhost', port='5432'):
        self.conn_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }

    @contextmanager
    def get_cursor(self):
        """Контекстный менеджер для работы с курсором"""
        conn = psycopg2.connect(**self.conn_params)
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_parts(self, search: str = '', brand: str = '',
                  condition: str = '', location: str = '',
                  in_stock_only: bool = False) -> List[Part]:
        """Получить список запчастей с фильтрацией"""
        with self.get_cursor() as cur:
            query = """
                SELECT id, oem_number, part_name, photo_url,
                       brand, model, price, quantity, condition,
                       address, store_name, phone, body_code, 
                       year_start, year_end
                FROM parts_inventory
                WHERE 1=1
            """
            params = []

            if search:
                query += """ AND (oem_number ILIKE %s OR part_name ILIKE %s 
                           OR brand ILIKE %s OR model ILIKE %s)"""
                search_pattern = f'%{search}%'
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

            if brand and brand != 'Все марки':
                query += " AND brand ILIKE %s"
                params.append(f'%{brand}%')

            if condition and condition != 'Любое состояние':
                query += " AND condition = %s"
                params.append(condition.lower())

            if in_stock_only:
                query += " AND quantity > 0"

            query += " ORDER BY id"
            cur.execute(query, params)

            parts = []
            for row in cur.fetchall():
                parts.append(Part(
                    id=row[0],
                    oem_number=row[1],
                    part_name=row[2],
                    photo_url=row[3],
                    brand=row[4],
                    model=row[5],
                    price=Decimal(row[6]) if row[6] else Decimal(0),
                    quantity=row[7] or 0,
                    condition=row[8] or 'new',
                    address=row[9],
                    store_name=row[10],
                    phone=row[11],
                    body_code=row[12],
                    year_start=row[13],
                    year_end=row[14]
                ))
            return parts

    def get_inventory(self) -> List[InventoryItem]:
        """Получить список инвентаря"""
        with self.get_cursor() as cur:
            query = """
                SELECT part_name, oem_number, 
                       COALESCE(brand, '') || ' ' || COALESCE(model, '') as car_model,
                       price, quantity, address
                FROM parts_inventory
                ORDER BY store_name, part_name
            """
            cur.execute(query)

            items = []
            for row in cur.fetchall():
                items.append(InventoryItem(
                    part_name=row[0],
                    oem_number=row[1],
                    car_model=row[2].strip() or "Не указано",
                    price=Decimal(row[3]) if row[3] else Decimal(0),
                    quantity=row[4] or 0,
                    address=row[5] or ""
                ))
            return items

    def get_all_brands(self) -> List[str]:
        """Получить все уникальные марки"""
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT brand 
                FROM parts_inventory 
                WHERE brand IS NOT NULL AND brand != ''
                ORDER BY brand
            """)
            return [row[0] for row in cur.fetchall()]

    def get_all_locations(self) -> List[str]:
        """Получить все уникальные адреса"""
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT address 
                FROM parts_inventory 
                WHERE address IS NOT NULL AND address != ''
                ORDER BY address
            """)
            return [row[0] for row in cur.fetchall()]

    def add_part(self, data: Dict[str, Any]) -> int:
        """Добавить новую запчасть"""
        with self.get_cursor() as cur:
            query = """
                INSERT INTO parts_inventory (
                    oem_number, part_name, photo_url,
                    brand, model, body_code, year_start, year_end,
                    address, store_name, phone,
                    quantity, price, condition
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            cur.execute(query, (
                data['oem_number'], data['part_name'], data.get('photo_url'),
                data['brand'], data['model'], data.get('body_code'),
                data.get('year_start'), data.get('year_end'),
                data['address'], data['store_name'], data.get('phone'),
                data['quantity'], data['price'], data['condition']
            ))
            return cur.fetchone()[0]

    def update_part(self, part_id: int, data: Dict[str, Any]) -> bool:
        """Обновить запчасть"""
        with self.get_cursor() as cur:
            query = """
                UPDATE parts_inventory SET
                    oem_number = %s, part_name = %s, photo_url = %s,
                    brand = %s, model = %s, body_code = %s,
                    year_start = %s, year_end = %s,
                    address = %s, store_name = %s, phone = %s,
                    quantity = %s, price = %s, condition = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id
            """
            cur.execute(query, (
                data['oem_number'], data['part_name'], data.get('photo_url'),
                data['brand'], data['model'], data.get('body_code'),
                data.get('year_start'), data.get('year_end'),
                data['address'], data['store_name'], data.get('phone'),
                data['quantity'], data['price'], data['condition'],
                part_id
            ))
            return cur.fetchone() is not None

    def delete_part(self, part_id: int) -> bool:
        """Удалить запчасть"""
        with self.get_cursor() as cur:
            cur.execute("DELETE FROM parts_inventory WHERE id = %s RETURNING id", (part_id,))
            return cur.fetchone() is not None

    def get_part_by_id(self, part_id: int) -> Optional[Part]:
        """Получить запчасть по ID"""
        with self.get_cursor() as cur:
            cur.execute("SELECT * FROM parts_inventory WHERE id = %s", (part_id,))
            row = cur.fetchone()
            if row:
                return Part(
                    id=row[0],
                    oem_number=row[1],
                    part_name=row[2],
                    photo_url=row[3],
                    brand=row[4],
                    model=row[5],
                    price=Decimal(row[13]) if row[13] else Decimal(0),
                    quantity=row[12] or 0,
                    condition=row[14] or 'new',
                    address=row[9],
                    store_name=row[10],
                    phone=row[11],
                    body_code=row[6],
                    year_start=row[7],
                    year_end=row[8]
                )
            return None