from typing import List, Optional, Dict, Any
from decimal import Decimal
from models import Part, InventoryItem
from database import Database


class PartController:
    """Контроллер для управления запчастями (business logic)"""

    def __init__(self):
        self.db = Database()

    def get_all_parts(self, search: str = '', brand: str = '',
                      condition: str = '', location: str = '',
                      in_stock_only: bool = False) -> List[Part]:
        """Получить все запчасти с фильтрацией"""
        return self.db.get_parts(search, brand, condition, location, in_stock_only)

    def get_inventory(self) -> List[InventoryItem]:
        """Получить инвентарь"""
        return self.db.get_inventory()

    def get_brands(self) -> List[str]:
        """Получить список марок"""
        return self.db.get_all_brands()

    def get_locations(self) -> List[str]:
        """Получить список локаций"""
        return self.db.get_all_locations()

    def add_part(self, data: Dict[str, Any]) -> bool:
        """Добавить запчасть"""
        try:
            if not data.get('oem_number') or not data.get('part_name'):
                raise ValueError("OEM номер и название обязательны")

            if data.get('price', 0) < 0:
                raise ValueError("Цена не может быть отрицательной")

            if data.get('quantity', 0) < 0:
                raise ValueError("Количество не может быть отрицательным")

            condition = data.get('condition', 'new').lower()
            if condition not in ['new', 'used']:
                raise ValueError("Состояние должно быть 'new' или 'used'")

            data['condition'] = condition
            data['price'] = Decimal(str(data['price']))

            self.db.add_part(data)
            return True
        except Exception as e:
            raise Exception(f"Ошибка при добавлении: {e}")

    def update_part(self, part_id: int, data: Dict[str, Any]) -> bool:
        """Обновить запчасть"""
        try:
            if data.get('price', 0) < 0:
                raise ValueError("Цена не может быть отрицательной")

            if data.get('quantity', 0) < 0:
                raise ValueError("Количество не может быть отрицательным")

            condition = data.get('condition', 'new').lower()
            if condition not in ['new', 'used']:
                raise ValueError("Состояние должно быть 'new' или 'used'")

            data['condition'] = condition
            data['price'] = Decimal(str(data['price']))

            return self.db.update_part(part_id, data)
        except Exception as e:
            raise Exception(f"Ошибка при обновлении: {e}")

    def delete_part(self, part_id: int) -> bool:
        """Удалить запчасть"""
        return self.db.delete_part(part_id)

    def get_part(self, part_id: int) -> Optional[Part]:
        """Получить запчасть по ID"""
        return self.db.get_part_by_id(part_id)