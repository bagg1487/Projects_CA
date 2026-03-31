import psycopg2
from decimal import Decimal
from datetime import datetime


def mergesort(data, key_func, reverse=False):
    """Сортировка слиянием по заданному ключу"""
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    left = mergesort(data[:mid], key_func, reverse)
    right = mergesort(data[mid:], key_func, reverse)
    
    return merge(left, right, key_func, reverse)


def merge(left, right, key_func, reverse):
    """Слияние двух отсортированных списков"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        left_val = key_func(left[i])
        right_val = key_func(right[j])
        
        if reverse:
            if left_val >= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            if left_val <= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


class TreeNode:
    """Узел дерева оптимального поиска"""
    def __init__(self, oem, record, left=None, right=None):
        self.oem = oem
        self.record = record
        self.left = left
        self.right = right


def build_optimal_bst(records):
    """
    Построение оптимального бинарного дерева поиска (алгоритм А2)
    на основе отсортированных OEM-номеров.
    """
    if not records:
        return None

    sorted_records = sorted(records, key=lambda x: x['oem_number'])

    return build_balanced_bst(sorted_records, 0, len(sorted_records) - 1)


def build_balanced_bst(sorted_records, start, end):
    """Рекурсивное построение сбалансированного BST"""
    if start > end:
        return None
    
    mid = (start + end) // 2
    record = sorted_records[mid]
    
    node = TreeNode(
        oem=record['oem_number'],
        record=record,
        left=build_balanced_bst(sorted_records, start, mid - 1),
        right=build_balanced_bst(sorted_records, mid + 1, end)
    )
    return node


def search_in_bst(node, oem_query):
    """Поиск по OEM-номеру в дереве"""
    if node is None:
        return None
    
    oem_upper = node.oem.upper()
    query_upper = oem_query.upper()
    
    if oem_upper == query_upper:
        return node.record
    elif query_upper < oem_upper:
        return search_in_bst(node.left, oem_query)
    else:
        return search_in_bst(node.right, oem_query)


def inorder_traversal(node, result=None):
    """Обход дерева (in-order) для вывода"""
    if result is None:
        result = []
    if node:
        inorder_traversal(node.left, result)
        result.append(node.record)
        inorder_traversal(node.right, result)
    return result



def get_connection():
    """Подключение к БД"""
    return psycopg2.connect(
        dbname="parts_catalog",
        user="myuser",
        password="mypassword",
        host="localhost",
        port="5432"
    )


def fetch_all_parts():
    """Получить все запчасти из БД"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM parts_inventory ORDER BY id")
    
    columns = [desc[0] for desc in cur.description]
    parts = [dict(zip(columns, row)) for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    return parts


def add_part():
    """Добавить новую запчасть"""
    print("\n--- Добавление запчасти ---")
    
    oem_number = input("OEM-номер: ").strip()
    part_name = input("Название запчасти: ").strip()
    photo_url = input("URL фото (оставьте пустым, если нет): ").strip() or None
    
    brand = input("Марка авто: ").strip()
    model = input("Модель авто: ").strip()
    body_code = input("Код кузова (например, RD1): ").strip() or None
    year_start = input("Год начала выпуска: ").strip() or "1845"
    while not (year_start.isnumeric() and int(year_start) > 1845 and int(year_start) <= datetime.now().year):
        year_start = input("Некорректный ввод (Целое число больше 1845). Год начала выпуска: ").strip()  or "1845"
    year_end = input("Год окончания выпуска: ").strip() or str(datetime.now().year)
    while not (year_end.isnumeric() and int(year_end) >= int(year_start) and int(year_end) <= datetime.now().year):
        year_end = input("Некорретный ввод (Целое число больше года начала выпуска"
                         " и меньше либо равно нынешнему году). Год окончания выпуска: ").strip() or str(datetime.now().year)

    address = input("Адрес магазина: ").strip()
    store_name = input("Название магазина: ").strip()
    phone = input("Телефон: ").strip() or None
    
    quantity = input("Количество: ").strip() or "1"
    while not (quantity.isnumeric() and int(quantity) >= 1):
        quantity = input("Некорретный ввод. Количество: ").strip() or "1"
    price = input("Цена: ").strip() or "0"
    while not (price.isnumeric() and int(price) >= 0):
        price = input("Некорретный ввод. Цена: ").strip() or "0"
    condition = input("Состояние (new/used): ").strip().lower()
    while not (condition.lower() == "new" or condition.lower() == "used"):
        condition = input("Состояние (new/used): ").strip().lower()

    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO parts_inventory (
                oem_number, part_name, photo_url,
                brand, model, body_code, year_start, year_end,
                address, store_name, phone,
                quantity, price, condition
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, oem_number, part_name;
        """, (
            oem_number, part_name, photo_url,
            brand, model, body_code,
            int(year_start) if year_start else None,
            int(year_end) if year_end else None,
            address, store_name, phone,
            int(quantity) if quantity else 0,
            Decimal(price), condition
        ))
        
        result = cur.fetchone()
        conn.commit()
        print(f"Запчасть добавлена: ID={result[0]}, OEM={result[1]}, Название={result[2]}")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def delete_part():
    """Удалить запчасть по ID"""
    print("\n--- Удаление запчасти ---")
    part_id = input("Введите ID запчасти для удаления: ").strip()
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM parts_inventory WHERE id = %s RETURNING id, oem_number", (part_id,))
        result = cur.fetchone()
        conn.commit()
        
        if result:
            print(f"Удалена запчасть: ID={result[0]}, OEM={result[1]}")
        else:
            print("Запчасть с таким ID не найдена")
            
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def edit_part():
    """Редактировать запчасть"""
    print("\n--- Редактирование запчасти ---")
    part_id = input("Введите ID запчасти для редактирования: ").strip()
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM parts_inventory WHERE id = %s", (part_id,))
        columns = [desc[0] for desc in cur.description]
        part = dict(zip(columns, cur.fetchone()))
        
        if not part:
            print("Запчасть не найдена")
            return
        
        print(f"\nТекущие данные: {part['oem_number']} - {part['part_name']}")
        print("Нажмите Enter, чтобы оставить текущее значение")
        
        new_oem = input(f"OEM-номер [{part['oem_number']}]: ").strip() or part['oem_number']
        new_name = input(f"Название [{part['part_name']}]: ").strip() or part['part_name']
        new_price = input(f"Цена [{part['price']}]: ").strip() or part['price']
        new_qty = input(f"Количество [{part['quantity']}]: ").strip() or part['quantity']
        new_condition = input(f"Состояние [{part['condition']}]: ").strip() or part['condition']
        
        cur.execute("""
            UPDATE parts_inventory SET
                oem_number = %s, part_name = %s, price = %s,
                quantity = %s, condition = %s, updated_at = NOW()
            WHERE id = %s
        """, (new_oem, new_name, Decimal(new_price), int(new_qty), new_condition.lower(), part_id))
        
        conn.commit()
        print("Запчасть обновлена")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def print_parts(parts, page_size=10):
    """Вывод записей по 10 штук с запросом на продолжение"""
    if not parts:
        print("Запчасти не найдены")
        return
    
    total_pages = (len(parts) + page_size - 1) // page_size
    current_page = 1

    while current_page <= total_pages:
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, len(parts))

        print(f"\nНайдено записей: {len(parts)} (показаны {start_idx + 1}-{end_idx})")
        print("-" * 100)

        for p in parts[start_idx:end_idx]:
            print(f"ID: {p['id']}")
            print(f"  OEM: {p['oem_number']} | Название: {p['part_name']}")
            print(f"  Авто: {p['brand']} {p['model']} {p['body_code'] or ''} ({p['year_start'] or '?'}-{p['year_end'] or '?'})")
            print(f"  Магазин: {p['store_name']} | Адрес: {p['address']}")
            print(f"  Цена: {p['price']} | Кол-во: {p['quantity']} | Состояние: {p['condition']}")
            print("-" * 100)

        if current_page < total_pages:
            choice = input("\nПоказать следующие 10 записей? (y/n): ").strip().lower()
            if choice == 'y' or choice == 'да':
                current_page += 1
            else:
                break
        else:
            break


# ==================== МЕНЮ ====================

def menu_view_all():
    """Просмотр всех запчастей"""
    print("\n=== Все запчасти ===")
    parts = fetch_all_parts()
    print_parts(parts)


def menu_add():
    """Добавление запчасти"""
    add_part()


def menu_search():
    """Поиск запчастей"""
    print("\n--- Поиск ---")
    print("1) По OEM-номеру")
    print("2) По марке/модели")
    print("3) По году выпуска")
    
    choice = input("Выберите тип поиска (1-3): ").strip()
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        if choice == '1':
            oem = input("OEM-номер: ").strip()
            cur.execute("SELECT * FROM parts_inventory WHERE oem_number ILIKE %s", (f"%{oem}%",))
        elif choice == '2':
            brand = input("Марка: ").strip()
            model = input("Модель: ").strip()
            query = "SELECT * FROM parts_inventory WHERE 1=1"
            params = []
            if brand:
                query += " AND brand ILIKE %s"
                params.append(f"%{brand}%")
            if model:
                query += " AND model ILIKE %s"
                params.append(f"%{model}%")
            cur.execute(query, params)
        elif choice == '3':
            year = input("Год: ").strip()
            cur.execute("""
                SELECT * FROM parts_inventory 
                WHERE year_start <= %s AND year_end >= %s
            """, (year, year))
        else:
            print("Неверный выбор")
            return
        
        columns = [desc[0] for desc in cur.description]
        parts = [dict(zip(columns, row)) for row in cur.fetchall()]
        print_parts(parts)
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        cur.close()
        conn.close()


def menu_sort():
    """Сортировка запчастей"""
    print("\n--- Сортировка ---")
    print("Доступные поля:")
    print("1) Цена")
    print("2) OEM-номер")
    print("3) Год выпуска")
    print("4) Состояние")
    print("0) Все поля (последовательно)")
    
    choices = input("Выберите поля (например: 1,2,3 или 0): ").strip()
    order = input("Порядок (asc/desc): ").strip().lower()
    reverse = (order == 'desc')
    
    parts = fetch_all_parts()
    
    if not parts:
        print("Нет данных для сортировки")
        return

    sort_keys = {
        '1': lambda x: float(x['price']) if x['price'] else 0,
        '2': lambda x: x['oem_number'] or '',
        '3': lambda x: x['year_start'] or 0,
        '4': lambda x: x['condition'] or ''
    }
    
    if choices == '0':

        for key in ['1', '2', '3', '4']:
            parts = mergesort(parts, sort_keys[key], reverse)
    else:

        for choice in choices.replace(' ', '').split(','):
            if choice in sort_keys:
                parts = mergesort(parts, sort_keys[choice], reverse)
    
    print_parts(parts)


def menu_bst_search():
    """Поиск через дерево оптимального поиска"""
    print("\n--- Поиск через дерево (ДОП А2) ---")
    
    parts = fetch_all_parts()
    if not parts:
        print("Нет данных для построения дерева")
        return

    bst_root = build_optimal_bst(parts)
    print(f"Дерево построено ({len(parts)} записей)")

    oem_query = input("Введите OEM-номер для поиска: ").strip()
    result = search_in_bst(bst_root, oem_query)
    
    if result:
        print("\nНайдено:")
        print(f"  OEM: {result['oem_number']} | Название: {result['part_name']}")
        print(f"  Цена: {result['price']} | Состояние: {result['condition']}")
    else:
        print("Не найдено")


def menu_delete():
    """Удаление запчасти"""
    delete_part()


def menu_edit():
    """Редактирование запчасти"""
    edit_part()


def main():
    """Главное меню"""
    while True:
        print("\n========== УПРАВЛЕНИЕ ЗАПЧАСТЯМИ ==========")
        print("1) Просмотр всех запчастей")
        print("2) Добавление запчасти")
        print("3) Поиск запчастей")
        print("4) Сортировка (Mergesort)")
        print("5) Поиск через дерево (ДОП А2)")
        print("6) Удаление запчасти")
        print("7) Редактирование запчасти")
        print("0) Выход")
        
        choice = input("\nВыберите пункт (0-7): ").strip()
        
        actions = {
            '1': menu_view_all,
            '2': menu_add,
            '3': menu_search,
            '4': menu_sort,
            '5': menu_bst_search,
            '6': menu_delete,
            '7': menu_edit,
        }
        
        if choice == '0':
            print("Выход")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
