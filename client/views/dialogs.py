from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from typing import Dict, Any, Optional
from models import Part


class PartDialog(QDialog):
    """Диалог для добавления/редактирования запчасти"""

    def __init__(self, parent=None, part: Optional[Part] = None):
        super().__init__(parent)
        self.part = part
        self.setupUI()

        if part:
            self.setWindowTitle("Редактирование запчасти")
            self.loadData()
        else:
            self.setWindowTitle("Добавление запчасти")

    def setupUI(self):
        self.setMinimumWidth(400)
        layout = QFormLayout(self)

        self.oemEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.brandEdit = QLineEdit()
        self.modelEdit = QLineEdit()

        self.priceSpin = QDoubleSpinBox()
        self.priceSpin.setRange(0, 999999)
        self.priceSpin.setDecimals(2)

        self.quantitySpin = QSpinBox()
        self.quantitySpin.setRange(0, 9999)

        self.conditionCombo = QComboBox()
        self.conditionCombo.addItems(["new", "used"])

        self.addressEdit = QLineEdit()
        self.storeEdit = QLineEdit()

        layout.addRow("OEM-номер:", self.oemEdit)
        layout.addRow("Название:", self.nameEdit)
        layout.addRow("Марка:", self.brandEdit)
        layout.addRow("Модель:", self.modelEdit)
        layout.addRow("Цена:", self.priceSpin)
        layout.addRow("Количество:", self.quantitySpin)
        layout.addRow("Состояние:", self.conditionCombo)
        layout.addRow("Адрес:", self.addressEdit)
        layout.addRow("Магазин:", self.storeEdit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def loadData(self):
        """Загрузить данные запчасти в поля"""
        if self.part:
            self.oemEdit.setText(self.part.oem_number)
            self.nameEdit.setText(self.part.part_name)
            self.brandEdit.setText(self.part.brand or "")
            self.modelEdit.setText(self.part.model or "")
            self.priceSpin.setValue(float(self.part.price))
            self.quantitySpin.setValue(self.part.quantity)
            self.conditionCombo.setCurrentText(self.part.condition)
            self.addressEdit.setText(self.part.address or "")
            self.storeEdit.setText(self.part.store_name or "")

    def getData(self) -> Dict[str, Any]:
        """Получить данные из полей"""
        return {
            'oem_number': self.oemEdit.text(),
            'part_name': self.nameEdit.text(),
            'brand': self.brandEdit.text(),
            'model': self.modelEdit.text(),
            'price': self.priceSpin.value(),
            'quantity': self.quantitySpin.value(),
            'condition': self.conditionCombo.currentText(),
            'address': self.addressEdit.text(),
            'store_name': self.storeEdit.text(),
            'photo_url': None,
            'body_code': None,
            'year_start': None,
            'year_end': None,
            'phone': None
        }