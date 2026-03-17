import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

class Database:
    def __init__(self, dbname='parts_catalog', user='myuser', password='', host='localhost', port='5432'):
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
        with self.get_cursor() as cur:
            query = """
                SELECT p.oem, p.name, cm.brand || ' ' || cm.model as car_model, p.photo_url
                FROM parts p
                LEFT JOIN part_compatibility pc ON p.id = pc.part_id
                LEFT JOIN car_models cm ON pc.model_id = cm.id
                WHERE 1=1
            """
            params = []
            
            if search:
                query += " AND (p.oem ILIKE %s OR p.name ILIKE %s OR cm.brand ILIKE %s)"
                search_pattern = f'%{search}%'
                params.extend([search_pattern, search_pattern, search_pattern])
            
            if condition and condition != 'Любое состояние':
                query += " AND p.condition = %s"
                params.append(condition)
            
            cur.execute(query, params)
            return cur.fetchall()
    
    def get_inventory(self):
        with self.get_cursor() as cur:
            query = """
                SELECT p.name, p.oem, cm.brand || ' ' || cm.model as car_model,
                       i.price, i.quantity, l.address
                FROM inventory i
                JOIN parts p ON i.part_id = p.id
                JOIN locations l ON i.location_id = l.id
                LEFT JOIN part_compatibility pc ON p.id = pc.part_id
                LEFT JOIN car_models cm ON pc.model_id = cm.id
            """
            cur.execute(query)
            return cur.fetchall()