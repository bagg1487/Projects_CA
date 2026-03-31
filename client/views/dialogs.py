from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox,
    QDialogButtonBox, QLabel, QScrollArea, QWidget,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QPixmap
from typing import Dict, Any, Optional
from models import Part
import subprocess
import sys


def open_url(url: str):
    """Открыть URL в браузере (кросс-платформенно + WSL)"""
    try:
        subprocess.run(['wslview', url], check=True)
        return
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    try:
        subprocess.run(['cmd.exe', '/C', 'start', '', url])
        return
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    QDesktopServices.openUrl(QUrl(url))


class PartDialog(QDialog):
    """Диалог для добавления/редактирования запчасти"""

    def __init__(self, parent=None, part: Optional[Part] = None):
        super().__init__(parent)
        self.part = part
        self.setModal(True)
        self.setupUI()

        if part:
            self.setWindowTitle("✏️  Редактирование запчасти")
            self.loadData()
        else:
            self.setWindowTitle("➕  Добавление запчасти")

    def setupUI(self):
        self.setMinimumWidth(480)
        self.resize(500, 640)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        def make_line(placeholder=''):
            w = QLineEdit()
            if placeholder:
                w.setPlaceholderText(placeholder)
            return w

        self.oemEdit       = make_line('Обязательное поле')
        self.nameEdit      = make_line('Обязательное поле')
        self.brandEdit     = make_line('Toyota, BMW, …')
        self.modelEdit     = make_line('Camry, E46, …')
        self.bodyEdit      = make_line('ACV40, E46, …')
        self.yearStartEdit = make_line('2005')
        self.yearEndEdit   = make_line('2012')
        self.addressEdit   = make_line('г. Алматы, ул. …')
        self.storeEdit     = make_line('Название магазина')
        self.phoneEdit     = make_line('+7 (777) …')

        shopRow = QHBoxLayout()
        self.shopUrlEdit = make_line('https://…')
        self.openUrlBtn = QPushButton('🔗')
        self.openUrlBtn.setFixedWidth(36)
        self.openUrlBtn.setToolTip('Открыть ссылку в браузере')
        self.openUrlBtn.clicked.connect(self._open_shop_url)
        shopRow.addWidget(self.shopUrlEdit)
        shopRow.addWidget(self.openUrlBtn)

        photoRow = QHBoxLayout()
        self.photoEdit = make_line('https://… (ссылка на изображение)')
        self.previewBtn = QPushButton('🖼')
        self.previewBtn.setFixedWidth(36)
        self.previewBtn.setToolTip('Открыть фото в браузере')
        self.previewBtn.clicked.connect(self._open_photo)
        photoRow.addWidget(self.photoEdit)
        photoRow.addWidget(self.previewBtn)

        self.priceSpin = QDoubleSpinBox()
        self.priceSpin.setRange(0, 99_999_999)
        self.priceSpin.setDecimals(2)
        self.priceSpin.setSuffix(' ₸')

        self.quantitySpin = QSpinBox()
        self.quantitySpin.setRange(0, 999_999)

        self.conditionCombo = QComboBox()
        self.conditionCombo.addItems(['new', 'used'])

        form.addRow('OEM-номер *:', self.oemEdit)
        form.addRow('Название *:', self.nameEdit)
        form.addRow('Марка:', self.brandEdit)
        form.addRow('Модель:', self.modelEdit)
        form.addRow('Кузов:', self.bodyEdit)
        form.addRow('Год (с):', self.yearStartEdit)
        form.addRow('Год (по):', self.yearEndEdit)
        form.addRow('Адрес:', self.addressEdit)
        form.addRow('Магазин:', self.storeEdit)
        form.addRow('Телефон:', self.phoneEdit)
        form.addRow('Ссылка на магазин:', shopRow)
        form.addRow('Фото (URL):', photoRow)
        form.addRow('Цена:', self.priceSpin)
        form.addRow('Количество:', self.quantitySpin)
        form.addRow('Состояние:', self.conditionCombo)

        layout.addLayout(form)

        scroll.setWidget(inner)
        outer.addWidget(scroll)

        btnBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btnBox.button(QDialogButtonBox.StandardButton.Ok).setText('Сохранить')
        btnBox.button(QDialogButtonBox.StandardButton.Cancel).setText('Отмена')
        btnBox.accepted.connect(self.accept)
        btnBox.rejected.connect(self.reject)

        btnLayout = QHBoxLayout()
        btnLayout.setContentsMargins(24, 10, 24, 16)
        btnLayout.addWidget(btnBox)
        outer.addLayout(btnLayout)

    def _open_shop_url(self):
        url = self.shopUrlEdit.text().strip()
        if url:
            open_url(url)
        else:
            QMessageBox.information(self, 'Нет ссылки', 'Введите ссылку на магазин.')

    def _open_photo(self):
        url = self.photoEdit.text().strip()
        if url:
            open_url(url)
        else:
            QMessageBox.information(self, 'Нет фото', 'Введите URL изображения.')

    def loadData(self):
        if not self.part:
            return
        p = self.part
        self.oemEdit.setText(p.oem_number or '')
        self.nameEdit.setText(p.part_name or '')
        self.brandEdit.setText(p.brand or '')
        self.modelEdit.setText(p.model or '')
        self.bodyEdit.setText(p.body_code or '')
        self.yearStartEdit.setText(str(p.year_start) if p.year_start else '')
        self.yearEndEdit.setText(str(p.year_end) if p.year_end else '')
        self.addressEdit.setText(p.address or '')
        self.storeEdit.setText(p.store_name or '')
        self.phoneEdit.setText(p.phone or '')
        self.shopUrlEdit.setText(p.shop_url or '')
        self.photoEdit.setText(p.photo_url or '')
        self.priceSpin.setValue(float(p.price))
        self.quantitySpin.setValue(p.quantity)
        idx = self.conditionCombo.findText(p.condition)
        if idx >= 0:
            self.conditionCombo.setCurrentIndex(idx)

    def getData(self) -> Dict[str, Any]:
        def _int(text):
            try:
                return int(text.strip()) if text.strip() else None
            except ValueError:
                return None

        return {
            'oem_number':  self.oemEdit.text().strip(),
            'part_name':   self.nameEdit.text().strip(),
            'brand':       self.brandEdit.text().strip() or None,
            'model':       self.modelEdit.text().strip() or None,
            'body_code':   self.bodyEdit.text().strip() or None,
            'year_start':  _int(self.yearStartEdit.text()),
            'year_end':    _int(self.yearEndEdit.text()),
            'address':     self.addressEdit.text().strip() or None,
            'store_name':  self.storeEdit.text().strip() or None,
            'phone':       self.phoneEdit.text().strip() or None,
            'shop_url':    self.shopUrlEdit.text().strip() or None,
            'photo_url':   self.photoEdit.text().strip() or None,
            'price':       self.priceSpin.value(),
            'quantity':    self.quantitySpin.value(),
            'condition':   self.conditionCombo.currentText(),
        }