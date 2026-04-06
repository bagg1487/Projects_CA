from typing import List, Optional, Dict, Any
from decimal import Decimal
from models import Part, InventoryItem
from database import Database
from utils.algorithms import OptimalBST, binary_search_name, mergesort


class PartController:

    def __init__(self):
        self.db = Database()
        self._all_parts: List[Part] = []
        self._bst_oem      = OptimalBST()
        self._bst_brand    = OptimalBST()
        self._bst_model    = OptimalBST()
        self._sorted_by_name: List[Part] = []
        self._index_dirty  = True

    def _rebuild_index(self, parts: List[Part]) -> None:
        self._all_parts = parts
        self._bst_oem.build(parts,   'oem_number')
        self._bst_brand.build(parts, 'brand')
        self._bst_model.build(parts, 'model')
        self._sorted_by_name = mergesort(
            list(parts),
            lambda p: (p.part_name or '').upper()
        )
        self._index_dirty = False

    def _filter_in_memory(self, parts: List[Part],
                          search: str, brand: str,
                          condition: str, location: str,
                          in_stock_only: bool) -> List[Part]:
        id_to_part = {id(p): p for p in parts}

        if search:
            q = search.strip()
            by_name  = set(id(p) for p in binary_search_name(self._sorted_by_name, q))
            by_oem   = set(id(p) for p in self._bst_oem.search_prefix(q))
            by_brand = set(id(p) for p in self._bst_brand.search_prefix(q))
            by_model = set(id(p) for p in self._bst_model.search_prefix(q))
            result   = by_name | by_oem | by_brand | by_model
        else:
            result = set(id_to_part.keys())

        if brand and brand != 'Все марки':
            brand_ids = set(id(p) for p in self._bst_brand.search_prefix(brand))
            result   &= brand_ids

        if condition and condition != 'Любое состояние':
            cond_lower = condition.lower()
            result = {pid for pid in result
                      if id_to_part[pid].condition == cond_lower}

        if location and location != 'Все склады':
            loc_up = location.upper()
            result = {pid for pid in result
                      if loc_up in (id_to_part[pid].store_name or '').upper()
                      or loc_up in (id_to_part[pid].address or '').upper()}

        if in_stock_only:
            result = {pid for pid in result if id_to_part[pid].quantity > 0}

        order = {id(p): i for i, p in enumerate(parts)}
        return sorted([id_to_part[pid] for pid in result],
                      key=lambda p: order.get(id(p), 0))

    def get_all_parts(self, search: str = '', brand: str = '',
                      condition: str = '', location: str = '',
                      in_stock_only: bool = False) -> List[Part]:
        if self._index_dirty:
            raw = self.db.get_parts()
            self._rebuild_index(raw)
        return self._filter_in_memory(
            self._all_parts, search, brand, condition, location, in_stock_only
        )

    def invalidate(self) -> None:
        self._index_dirty = True

    def get_inventory(self) -> List[InventoryItem]:
        return self.db.get_inventory()

    def get_brands(self) -> List[str]:
        return self.db.get_all_brands()

    def get_locations(self) -> List[str]:
        return self.db.get_all_locations()

    def add_part(self, data: Dict[str, Any]) -> bool:
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
            self.invalidate()
            return True
        except Exception as e:
            raise Exception(f"Ошибка при добавлении: {e}")

    def update_part(self, part_id: int, data: Dict[str, Any]) -> bool:
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
            result = self.db.update_part(part_id, data)
            self.invalidate()
            return result
        except Exception as e:
            raise Exception(f"Ошибка при обновлении: {e}")

    def delete_part(self, part_id: int) -> bool:
        result = self.db.delete_part(part_id)
        self.invalidate()
        return result

    def get_part(self, part_id: int) -> Optional[Part]:
        return self.db.get_part_by_id(part_id)