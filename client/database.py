import psycopg2
from contextlib import contextmanager
from decimal import Decimal
from typing import List, Optional, Dict, Any
from models import Part, InventoryItem


class Database:
    """Класс для работы с базой данных"""

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
                       year_start, year_end,
                       COALESCE(shop_url, '') as shop_url
                FROM parts_inventory
                WHERE 1=1
            """
            params = []

            if search:
                query += """ AND (oem_number ILIKE %s OR part_name ILIKE %s
                           OR brand ILIKE %s OR model ILIKE %s)"""
                sp = f'%{search}%'
                params.extend([sp, sp, sp, sp])

            if brand and brand != 'Все марки':
                query += " AND brand ILIKE %s"
                params.append(f'%{brand}%')

            if condition and condition != 'Любое состояние':
                query += " AND condition = %s"
                params.append(condition.lower())

            if location and location != 'Все склады':
                query += " AND (store_name ILIKE %s OR address ILIKE %s)"
                params.extend([f'%{location}%', f'%{location}%'])

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
                    year_end=row[14],
                    shop_url=row[15],
                ))
            return parts

    def get_inventory(self) -> List[InventoryItem]:
        """Получить список инвентаря"""
        with self.get_cursor() as cur:
            query = """
                SELECT part_name, oem_number,
                       COALESCE(brand, '') || ' ' || COALESCE(model, '') as car_model,
                       price, quantity, address,
                       COALESCE(condition, 'new') as condition,
                       COALESCE(store_name, '') as store_name,
                       COALESCE(phone, '') as phone,
                       COALESCE(shop_url, '') as shop_url,
                       COALESCE(photo_url, '') as photo_url,
                       COALESCE(brand, '') as brand,
                       COALESCE(model, '') as model,
                       COALESCE(body_code, '') as body_code,
                       year_start, year_end
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
                    address=row[5] or "",
                    condition=row[6],
                    store_name=row[7],
                    phone=row[8],
                    shop_url=row[9],
                    photo_url=row[10],
                    brand=row[11],
                    model=row[12],
                    body_code=row[13],
                    year_start=row[14],
                    year_end=row[15],
                ))
            return items

    def get_all_brands(self) -> List[str]:
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT brand FROM parts_inventory
                WHERE brand IS NOT NULL AND brand != ''
                ORDER BY brand
            """)
            return [row[0] for row in cur.fetchall()]

    def get_all_locations(self) -> List[str]:
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT DISTINCT COALESCE(store_name, address) as loc
                FROM parts_inventory
                WHERE COALESCE(store_name, address) IS NOT NULL
                  AND COALESCE(store_name, address) != ''
                ORDER BY loc
            """)
            return [row[0] for row in cur.fetchall()]

    def add_part(self, data: Dict[str, Any]) -> int:
        with self.get_cursor() as cur:
            query = """
                INSERT INTO parts_inventory (
                    oem_number, part_name, photo_url,
                    brand, model, body_code, year_start, year_end,
                    address, store_name, phone, shop_url,
                    quantity, price, condition
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            cur.execute(query, (
                data['oem_number'], data['part_name'], data.get('photo_url'),
                data.get('brand'), data.get('model'), data.get('body_code'),
                data.get('year_start'), data.get('year_end'),
                data.get('address'), data.get('store_name'), data.get('phone'),
                data.get('shop_url'),
                data['quantity'], data['price'], data['condition']
            ))
            return cur.fetchone()[0]

    def update_part(self, part_id: int, data: Dict[str, Any]) -> bool:
        with self.get_cursor() as cur:
            allowed_fields = [
                'oem_number', 'part_name', 'photo_url', 'brand', 'model', 'body_code',
                'year_start', 'year_end', 'address', 'store_name', 'phone', 'shop_url',
                'quantity', 'price', 'condition'
            ]
            set_clauses = []
            values = []
            for field in allowed_fields:
                if field in data:
                    set_clauses.append(f"{field} = %s")
                    values.append(data[field])
            if not set_clauses:
                return True
            set_clauses.append("updated_at = NOW()")
            query = f"UPDATE parts_inventory SET {', '.join(set_clauses)} WHERE id = %s RETURNING id"
            values.append(part_id)
            cur.execute(query, values)
            return cur.fetchone() is not None

    def delete_part(self, part_id: int) -> bool:
        with self.get_cursor() as cur:
            cur.execute(
                "DELETE FROM parts_inventory WHERE id = %s RETURNING id",
                (part_id,)
            )
            return cur.fetchone() is not None

    def get_part_by_id(self, part_id: int) -> Optional[Part]:
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT id, oem_number, part_name, photo_url,
                       brand, model, body_code, year_start, year_end,
                       address, store_name, phone,
                       quantity, price, condition,
                       COALESCE(shop_url, '') as shop_url
                FROM parts_inventory WHERE id = %s
            """, (part_id,))
            row = cur.fetchone()
            if row:
                return Part(
                    id=row[0],
                    oem_number=row[1],
                    part_name=row[2],
                    photo_url=row[3],
                    brand=row[4],
                    model=row[5],
                    body_code=row[6],
                    year_start=row[7],
                    year_end=row[8],
                    address=row[9],
                    store_name=row[10],
                    phone=row[11],
                    quantity=row[12] or 0,
                    price=Decimal(row[13]) if row[13] else Decimal(0),
                    condition=row[14] or 'new',
                    shop_url=row[15],
                )
            return None