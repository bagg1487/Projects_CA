import test_bd
from decimal import Decimal


def test_sort_numbers():
    print("\n1. Тест сортировки чисел")
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    result = test_bd.mergesort(data, lambda x: x)
    print(f"   Было: {data}")
    print(f"   Стало: {result}")
    assert result == [1, 1, 2, 3, 4, 5, 6, 9]
    print("    OK")


def test_sort_strings():
    print("\n2. Тест сортировки строк")
    data = ['banana', 'apple', 'cherry', 'date']
    result = test_bd.mergesort(data, lambda x: x)
    print(f"   Было: {data}")
    print(f"   Стало: {result}")
    assert result == ['apple', 'banana', 'cherry', 'date']
    print("    OK")


def test_sort_descending():
    print("\n3. Тест сортировки по убыванию")
    data = [3, 1, 4, 1, 5]
    result = test_bd.mergesort(data, lambda x: x, reverse=True)
    print(f"   Было: {data}")
    print(f"   Стало: {result}")
    assert result == [5, 4, 3, 1, 1]
    print("    OK")


def test_sort_by_price():
    print("\n4. Тест сортировки запчастей по цене")
    parts = [
        {'name': 'Фильтр', 'price': 500},
        {'name': 'Колодки', 'price': 1200},
        {'name': 'Масло', 'price': 300}
    ]
    result = test_bd.mergesort(parts, lambda x: x['price'])
    print("   Результат:")
    for p in result:
        print(f"      {p['name']}: {p['price']}")
    assert result[0]['name'] == 'Масло'
    assert result[1]['name'] == 'Фильтр'
    assert result[2]['name'] == 'Колодки'
    print("    OK")


def test_sort_empty():
    print("\n5. Тест сортировки пустого списка")
    result = test_bd.mergesort([], lambda x: x)
    assert result == []
    print("    OK")


def test_sort_one_element():
    print("\n6. Тест сортировки одного элемента")
    result = test_bd.mergesort([42], lambda x: x)
    assert result == [42]
    print("    OK")



def test_tree_empty():
    print("\n7. Тест пустого дерева")
    root = test_bd.build_optimal_bst([])
    assert root is None
    print("    OK")


def test_tree_one_node():
    print("\n8. Тест дерева с одной записью")
    records = [{'oem_number': '12345', 'part_name': 'Тестовая деталь'}]
    root = test_bd.build_optimal_bst(records)
    assert root is not None
    assert root.oem == '12345'
    assert root.left is None
    assert root.right is None
    print("    OK")


def test_tree_search_found():
    print("\n9. Тест поиска существующей записи")
    records = [
        {'oem_number': 'B123', 'part_name': 'Деталь B'},
        {'oem_number': 'A123', 'part_name': 'Деталь A'},
        {'oem_number': 'C123', 'part_name': 'Деталь C'}
    ]
    root = test_bd.build_optimal_bst(records)
    result = test_bd.search_in_bst(root, 'A123')
    assert result is not None
    assert result['oem_number'] == 'A123'
    print("    Найдена A123")


def test_tree_search_not_found():
    print("\n10. Тест поиска отсутствующей записи")
    records = [
        {'oem_number': 'B123', 'part_name': 'Деталь B'},
        {'oem_number': 'A123', 'part_name': 'Деталь A'}
    ]
    root = test_bd.build_optimal_bst(records)
    result = test_bd.search_in_bst(root, 'XXX')
    assert result is None
    print("    XXX не найдена")


def test_tree_case_insensitive():
    print("\n11. Тест поиска без учёта регистра")
    records = [{'oem_number': 'ABC123', 'part_name': 'Тест'}]
    root = test_bd.build_optimal_bst(records)
    result = test_bd.search_in_bst(root, 'abc123')
    assert result is not None
    assert result['oem_number'] == 'ABC123'
    print("    OK")


def test_tree_inorder():
    print("\n12. Тест обхода дерева (in-order)")
    records = [
        {'oem_number': 'B123', 'part_name': 'B'},
        {'oem_number': 'A123', 'part_name': 'A'},
        {'oem_number': 'C123', 'part_name': 'C'}
    ]
    root = test_bd.build_optimal_bst(records)
    result = test_bd.inorder_traversal(root)
    oems = [r['oem_number'] for r in result]
    print(f"   Порядок обхода: {oems}")
    assert oems == sorted(oems)
    print("    OK")



def test_db_connection():
    print("\n13. Тест подключения к БД")
    try:
        conn = test_bd.get_connection()
        assert conn is not None
        conn.close()
        print("    Подключение успешно")
    except Exception as e:
        print(f"    Ошибка: {e}")
        raise


def test_fetch_all_parts():
    print("\n14. Тест получения всех запчастей")
    try:
        parts = test_bd.fetch_all_parts()
        print(f"   Найдено записей: {len(parts)}")
        assert isinstance(parts, list)
        print("    OK")
    except Exception as e:
        print(f"    Ошибка: {e}")
        raise


def test_print_parts():
    print("\n15. Тест вывода запчастей")
    test_parts = [
        {
            'id': 1,
            'oem_number': '12345A',
            'part_name': 'Тестовая деталь',
            'brand': 'Toyota',
            'model': 'Camry',
            'body_code': 'XV50',
            'year_start': 2011,
            'year_end': 2018,
            'address': 'ул. Тестовая, 1',
            'store_name': 'Тестовый магазин',
            'phone': '123-456',
            'quantity': 10,
            'price': Decimal('500.00'),
            'condition': 'new'
        }
    ]
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    test_bd.print_parts(test_parts)
    output = sys.stdout.getvalue()
    
    sys.stdout = old_stdout
    
    assert "Найдено записей: 1" in output
    assert "Тестовая деталь" in output
    print("    Вывод работает")


def test_print_parts_empty():
    print("\n16. Тест вывода пустого списка")
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    test_bd.print_parts([])
    output = sys.stdout.getvalue()
    
    sys.stdout = old_stdout
    
    assert "Запчасти не найдены" in output
    print("    OK")



def test_merge_arrays():
    print("\n17. Тест слияния двух массивов")
    left = [1, 3, 5]
    right = [2, 4, 6]
    result = test_bd.merge(left, right, lambda x: x, reverse=False)
    print(f"   left: {left}")
    print(f"   right: {right}")
    print(f"   результат: {result}")
    assert result == [1, 2, 3, 4, 5, 6]
    print("    OK")


def test_merge_descending():
    print("\n18. Тест слияния в обратном порядке")
    left = [5, 3, 1]
    right = [6, 4, 2]
    result = test_bd.merge(left, right, lambda x: x, reverse=True)
    print(f"   left: {left}")
    print(f"   right: {right}")
    print(f"   результат: {result}")
    assert result == [6, 5, 4, 3, 2, 1]
    print("    OK")



if __name__ == "__main__":

    print("ТЕСТЫ")

    
    tests = [
        test_sort_numbers,
        test_sort_strings,
        test_sort_descending,
        test_sort_by_price,
        test_sort_empty,
        test_sort_one_element,
        test_tree_empty,
        test_tree_one_node,
        test_tree_search_found,
        test_tree_search_not_found,
        test_tree_case_insensitive,
        test_tree_inorder,
        test_db_connection,
        test_fetch_all_parts,
        test_print_parts,
        test_print_parts_empty,
        test_merge_arrays,
        test_merge_descending,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"    Ошибка: {e}")
            failed += 1
        except Exception as e:
            print(f"    Исключение: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"ИТОГО: {passed} пройдено, {failed} не пройдено")
    print("="*50)
    
    if failed == 0:
        print("\n ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
    else:
        print(f"\n {failed} тестов не прошло")