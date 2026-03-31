from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Part:
    """Модель запчасти"""
    id: int
    oem_number: str
    part_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    price: Decimal = Decimal(0)
    quantity: int = 0
    condition: str = 'new'
    address: Optional[str] = None
    store_name: Optional[str] = None
    photo_url: Optional[str] = None
    body_code: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None
    phone: Optional[str] = None
    shop_url: Optional[str] = None

    @property
    def car_info(self) -> str:
        """Получить информацию об автомобиле"""
        if self.brand or self.model:
            return f"{self.brand or ''} {self.model or ''}".strip()
        return "Не указано"

    @property
    def condition_display(self) -> str:
        """Отображение состояния"""
        return "NEW" if self.condition == 'new' else "USED"

    @property
    def years_display(self) -> str:
        """Отображение годов"""
        if self.year_start or self.year_end:
            return f"{self.year_start or '?'} – {self.year_end or '?'}"
        return ""


@dataclass
class InventoryItem:
    """Модель элемента инвентаря"""
    part_name: str
    oem_number: str
    car_model: str
    price: Decimal
    quantity: int
    address: str
    condition: str = 'new'
    store_name: str = ''
    phone: str = ''
    shop_url: str = ''
    photo_url: str = ''
    brand: str = ''
    model: str = ''
    body_code: str = ''
    year_start: Optional[int] = None
    year_end: Optional[int] = None