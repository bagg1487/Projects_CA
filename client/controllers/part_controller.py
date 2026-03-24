from typing import List, Optional, Dict, Any
from decimal import Decimal
from models import Part, InventoryItem


class PartController:
    """Заглушка контроллера для запчастей"""

    def __init__(self):
        print("PartController initialized (STUB)")
        # Пока не подключаем реальную БД
        self._mock_parts = self._create_mock_data()

    def _create_mock_data(self) -> List[Part]:
        """Создать тестовые данные"""
        return [
            Part(
                id=1,
                oem_number="12345-S12-123",
                part_name="Рама кузова",
                brand="Honda",
                model="CR-V",
                price=Decimal("5000.00"),
                quantity=3,
                condition="used",
                address="ул. Ленина, 15",
                store_name="Автозапчасти КZ"
            )
        ]

    def get_all_parts(self, search: str = '', brand: str = '',
                      condition: str = '', location: str = '',
                      in_stock_only: bool = False) -> List[Part]:
        """Получить все запчасти с фильтрацией (заглушка)"""
        parts = self._mock_parts

        if search:
            search_lower = search.lower()
            parts = [p for p in parts if
                     search_lower in p.oem_number.lower() or
                     search_lower in p.part_name.lower() or
                     (p.brand and search_lower in p.brand.lower()) or
                     (p.model and search_lower in p.model.lower())]

        if brand and brand != 'Все марки':
            parts = [p for p in parts if p.brand and brand.lower() in p.brand.lower()]

        if condition and condition != 'Любое состояние':
            parts = [p for p in parts if p.condition == condition.lower()]

        if in_stock_only:
            parts = [p for p in parts if p.quantity > 0]

        return parts

    def get_inventory(self) -> List[InventoryItem]:
        """Получить инвентарь (заглушка)"""
        inventory = []
        for part in self._mock_parts:
            inventory.append(InventoryItem(
                part_name=part.part_name,
                oem_number=part.oem_number,
                car_model=part.car_info,
                price=part.price,
                quantity=part.quantity,
                address=part.address or ""
            ))
        return inventory

    def get_brands(self) -> List[str]:
        """Получить список марок (заглушка)"""
        brands = list(set(p.brand for p in self._mock_parts if p.brand))
        return sorted(brands)

    def get_locations(self) -> List[str]:
        """Получить список локаций (заглушка)"""
        locations = list(set(p.address for p in self._mock_parts if p.address))
        return sorted(locations)

    def add_part(self, data: Dict[str, Any]) -> bool:
        """Добавить запчасть (заглушка)"""
        print(f"STUB: Adding part {data}")
        new_id = max([p.id for p in self._mock_parts]) + 1 if self._mock_parts else 1

        new_part = Part(
            id=new_id,
            oem_number=data['oem_number'],
            part_name=data['part_name'],
            brand=data.get('brand'),
            model=data.get('model'),
            price=Decimal(str(data['price'])),
            quantity=data.get('quantity', 0),
            condition=data.get('condition', 'new'),
            address=data.get('address'),
            store_name=data.get('store_name'),
            photo_url=data.get('photo_url'),
            body_code=data.get('body_code'),
            year_start=data.get('year_start'),
            year_end=data.get('year_end'),
            phone=data.get('phone')
        )
        self._mock_parts.append(new_part)
        return True

    def update_part(self, part_id: int, data: Dict[str, Any]) -> bool:
        """Обновить запчасть (заглушка)"""
        for i, part in enumerate(self._mock_parts):
            if part.id == part_id:
                updated_part = Part(
                    id=part_id,
                    oem_number=data['oem_number'],
                    part_name=data['part_name'],
                    brand=data.get('brand'),
                    model=data.get('model'),
                    price=Decimal(str(data['price'])),
                    quantity=data.get('quantity', 0),
                    condition=data.get('condition', 'new'),
                    address=data.get('address'),
                    store_name=data.get('store_name'),
                    photo_url=data.get('photo_url'),
                    body_code=data.get('body_code'),
                    year_start=data.get('year_start'),
                    year_end=data.get('year_end'),
                    phone=data.get('phone')
                )
                self._mock_parts[i] = updated_part
                return True
        return False

    def delete_part(self, part_id: int) -> bool:
        """Удалить запчасть (заглушка)"""
        for i, part in enumerate(self._mock_parts):
            if part.id == part_id:
                del self._mock_parts[i]
                return True
        return False

    def get_part(self, part_id: int) -> Optional[Part]:
        """Получить запчасть по ID (заглушка)"""
        for part in self._mock_parts:
            if part.id == part_id:
                return part
        return None