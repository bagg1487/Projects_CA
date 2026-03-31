from PyQt6 import sip
from utils.algorithms import mergesort
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QScrollArea, QFrame,
    QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter, QBrush
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from typing import List
from models import Part
from views.dialogs import open_url


SORT_OPTIONS = [
    ("По умолчанию",        None,        None),
    ("Цена: по возрастанию", "price",    False),
    ("Цена: по убыванию",   "price",     True),
    ("Название: А → Я",     "part_name", False),
    ("Название: Я → А",     "part_name", True),
    ("Марка: А → Я",        "brand",     False),
    ("Новинки",             "id",        True),
]


class ImageLoader(QObject):
    loaded = pyqtSignal(bytes, object)

    def __init__(self):
        super().__init__()
        self._manager = QNetworkAccessManager()
        self._manager.finished.connect(self._on_finished)
        self._pending = {}

    def load(self, url: str, label: QLabel):
        req = QNetworkRequest(QUrl(url))
        reply = self._manager.get(req)
        self._pending[reply] = label

    def _on_finished(self, reply):
        label = self._pending.get(reply)
        if not label:
            return

        if sip.isdeleted(label):
            del self._pending[reply]
            return

        if reply.error() == QNetworkReply.NetworkError.NoError:
            data = reply.readAll()
            pix = QPixmap()
            if pix.loadFromData(data):
                label.setPixmap(
                    pix.scaled(200, 160,
                               Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
                )

        del self._pending[reply]


def _placeholder_pixmap(w=200, h=160, dark=False) -> QPixmap:
    pix = QPixmap(w, h)
    bg = QColor('#2a2b30') if dark else QColor('#f1f3f5')
    pix.fill(bg)
    p = QPainter(pix)
    p.setPen(QColor('#5c5f66') if dark else QColor('#adb5bd'))
    f = QFont()
    f.setPointSize(28)
    p.setFont(f)
    p.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, '📷')
    p.end()
    return pix


class PartCard(QFrame):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, part: Part, image_loader: ImageLoader,
                 dark: bool = False, parent=None):
        super().__init__(parent)
        self.part = part
        self.dark = dark
        self._build(image_loader)
        self._apply_style()

    def _build(self, loader: ImageLoader):
        self.setFixedWidth(220)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 12)
        root.setSpacing(0)

        self.imgLabel = QLabel(self)
        self.imgLabel.setFixedSize(220, 160)
        self.imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imgLabel.setPixmap(_placeholder_pixmap(220, 160, self.dark))
        self.imgLabel.setScaledContents(False)

        if self.part.photo_url:
            loader.load(self.part.photo_url, self.imgLabel)

        root.addWidget(self.imgLabel)

        body = QVBoxLayout()
        body.setContentsMargins(12, 10, 12, 0)
        body.setSpacing(4)

        cond_color = '#2f9e44' if self.part.condition == 'new' else '#e67700'
        cond_text  = 'NEW' if self.part.condition == 'new' else 'USED'
        badge = QLabel(cond_text)
        badge.setFixedWidth(46)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background-color: {cond_color}; color: white; "
            f"border-radius: 4px; padding: 2px 0; font-size: 10px; font-weight: 700;"
        )

        name = QLabel(self.part.part_name)
        name.setWordWrap(True)
        name.setStyleSheet("font-weight: 700; font-size: 13px;")

        oem = QLabel(f"OEM: {self.part.oem_number}")
        oem.setStyleSheet("font-size: 11px; color: #868e96;")

        car = QLabel(self.part.car_info)
        car.setStyleSheet("font-size: 11px;")
        car.setWordWrap(True)

        if self.part.year_start or self.part.year_end:
            years = QLabel(f"📅 {self.part.years_display}")
            years.setStyleSheet("font-size: 11px; color: #868e96;")
        else:
            years = None

        price = QLabel(f"{self.part.price:,.0f} ₸")
        price.setStyleSheet("font-size: 16px; font-weight: 700; color: #e67700; margin-top: 4px;")

        qty_color = '#2f9e44' if self.part.quantity > 0 else '#fa5252'
        qty_text  = f"В наличии: {self.part.quantity}" if self.part.quantity > 0 else "Нет в наличии"
        qty = QLabel(qty_text)
        qty.setStyleSheet(f"font-size: 11px; color: {qty_color};")

        body.addWidget(badge)
        body.addSpacing(4)
        body.addWidget(name)
        body.addWidget(oem)
        body.addWidget(car)
        if years:
            body.addWidget(years)
        body.addWidget(price)
        body.addWidget(qty)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        btn_row.setContentsMargins(0, 8, 0, 0)

        if self.part.shop_url:
            shop_btn = QPushButton("🔗 Магазин")
            shop_btn.setProperty("cardBtn", True)
            shop_btn.clicked.connect(lambda: open_url(self.part.shop_url))
            btn_row.addWidget(shop_btn)

        edit_btn = QPushButton("✏")
        edit_btn.setFixedWidth(32)
        edit_btn.setProperty("cardBtn", True)
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.part.id))

        del_btn = QPushButton("🗑")
        del_btn.setFixedWidth(32)
        del_btn.setObjectName("deleteBtn")
        del_btn.setProperty("cardBtn", True)
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self.part.id))

        btn_row.addStretch()
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)

        body.addLayout(btn_row)
        root.addLayout(body)

    def _apply_style(self):
        if self.dark:
            self.setStyleSheet(
                "PartCard { background-color: #25262b; border: 1px solid #373a40; "
                "border-radius: 10px; } "
                "PartCard:hover { border: 1px solid #1c7ed6; } "
                "QPushButton[cardBtn=true] { padding: 5px 10px; font-size: 11px; } "
            )
        else:
            self.setStyleSheet(
                "PartCard { background-color: #ffffff; border: 1px solid #e9ecef; "
                "border-radius: 10px; } "
                "PartCard:hover { border: 1px solid #339af0; } "
                "QPushButton[cardBtn=true] { padding: 5px 10px; font-size: 11px; } "
            )


class CardView(QWidget):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    COLS = 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parts: List[Part] = []
        self._dark = False
        self._loader = ImageLoader()
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        sort_label = QLabel("Сортировка:")
        sort_label.setStyleSheet("font-size: 13px;")

        self.sortCombo = QComboBox()
        self.sortCombo.setMinimumWidth(200)
        for label, _, _ in SORT_OPTIONS:
            self.sortCombo.addItem(label)
        self.sortCombo.currentIndexChanged.connect(self._apply_sort)

        toolbar.addWidget(sort_label)
        toolbar.addWidget(self.sortCombo)
        toolbar.addStretch()

        self.countLabel = QLabel("")
        self.countLabel.setStyleSheet("color: #868e96; font-size: 12px;")
        toolbar.addWidget(self.countLabel)

        root.addLayout(toolbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._container = QWidget()
        self._grid = QGridLayout(self._container)
        self._grid.setSpacing(16)
        self._grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self._container)
        root.addWidget(scroll)

    def set_dark(self, dark: bool):
        self._dark = dark
        self.refresh()

    def set_parts(self, parts: List[Part]):
        self._parts = parts
        self._apply_sort()

    def _apply_sort(self):
        idx = self.sortCombo.currentIndex()
        _, key, reverse = SORT_OPTIONS[idx]

        if not key:
            self._render(self._parts)
            return

        def part_key_func(p):
            val = getattr(p, key)
            if val is None:
                return (2, "")

            if isinstance(val, (int, float)):
                return (0, float(val))

            text = str(val).strip()
            try:
                num_val = float(text.replace(' ', '').replace(',', '.'))
                return (0, num_val)
            except ValueError:
                return (1, text.lower())

        sorted_parts = mergesort(list(self._parts), part_key_func, reverse=bool(reverse))
        self._render(sorted_parts)

    def _render(self, parts: List[Part]):
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.countLabel.setText(f"Найдено: {len(parts)}")

        for i, part in enumerate(parts):
            card = PartCard(part, self._loader, self._dark)
            card.edit_requested.connect(self.edit_requested)
            card.delete_requested.connect(self.delete_requested)
            self._grid.addWidget(card, i // self.COLS, i % self.COLS)

    def refresh(self):
        self._apply_sort()
