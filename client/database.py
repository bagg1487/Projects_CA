import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

class Database:
    def __init__(self, dbname='parts_catalog', user='myuser', password='mypassword', host='localhost', port='5432'):
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

    def get_parts(self, search='', brand='', condition='', location='', in_stock_only=False):
        """Получить запчасти из единой таблицы parts_inventory"""
        with self.get_cursor() as cur:
            query = """
                SELECT oem_number, part_name, brand, model, body_code, 
                       year_start, year_end, photo_url, shop_url
                FROM parts_inventory
                WHERE 1=1
            """
            params = []

            if search:
                query += " AND (oem_number ILIKE %s OR part_name ILIKE %s OR brand ILIKE %s OR model ILIKE %s)"
                search_pattern = f'%{search}%'
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

            if brand:
                query += " AND brand ILIKE %s"
                params.append(f'%{brand}%')

            if condition and condition != 'Любое состояние':
                query += " AND condition = %s"
                params.append(condition)

            if location:
                query += " AND (store_name ILIKE %s OR address ILIKE %s)"
                location_pattern = f'%{location}%'
                params.extend([location_pattern, location_pattern])

            if in_stock_only:
                query += " AND quantity > 0"

            cur.execute(query, params)
            return cur.fetchall()

    def get_inventory(self):
        """Получить полный инвентарь из единой таблицы parts_inventory"""
        with self.get_cursor() as cur:
            query = """
                SELECT oem_number, part_name, brand, model, body_code,
                       year_start, year_end, price, quantity, condition,
                       store_name, address, phone, shop_url, photo_url
                FROM parts_inventory
                ORDER BY id
            """
            cur.execute(query)
            return cur.fetchall()

    def add_part(self, oem_number, part_name, brand, model, body_code,
                 year_start, year_end, address, store_name, phone, shop_url,
                 quantity, price, condition, photo_url=None):
        """Добавить новую запчасть"""
        with self.get_cursor() as cur:
            cur.execute("""
                INSERT INTO parts_inventory (
                    oem_number, part_name, photo_url,
                    brand, model, body_code, year_start, year_end,
                    address, store_name, phone, shop_url,
                    quantity, price, condition
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, oem_number, part_name
            """, (
                oem_number, part_name, photo_url,
                brand, model, body_code, year_start, year_end,
                address, store_name, phone, shop_url,
                quantity, price, condition
            ))
            return cur.fetchone()

    def update_part(self, part_id, **kwargs):
        """Обновить существующую запчасть"""
        allowed_fields = {
            'oem_number', 'part_name', 'photo_url', 'brand', 'model',
            'body_code', 'year_start', 'year_end', 'address', 'store_name',
            'phone', 'shop_url', 'quantity', 'price', 'condition'
        }
        
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
                params.append(value)
        
        if not updates:
            return None
        
        updates.append(sql.SQL("updated_at = NOW()"))
        params.append(part_id)
        
        query = sql.SQL("UPDATE parts_inventory SET {} WHERE id = %s RETURNING id, oem_number, part_name").format(
            sql.SQL(', ').join(updates)
        )
        
        with self.get_cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def delete_part(self, part_id):
        """Удалить запчасть по ID"""
        with self.get_cursor() as cur:
            cur.execute("DELETE FROM parts_inventory WHERE id = %s RETURNING id, oem_number", (part_id,))
            return cur.fetchone()

    def get_all_brands(self):
        """Получить список всех марок авто"""
        with self.get_cursor() as cur:
            cur.execute("SELECT DISTINCT brand FROM parts_inventory WHERE brand IS NOT NULL ORDER BY brand")
            return [row[0] for row in cur.fetchall()]

    def get_all_locations(self):
        """Получить список всех магазинов/адресов"""
        with self.get_cursor() as cur:
            cur.execute("SELECT DISTINCT store_name, address FROM parts_inventory ORDER BY store_name")
            return cur.fetchall()
