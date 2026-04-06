from PyQt6 import sip
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QScrollArea, QFrame,
    QComboBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QObject, QTimer, QSize
from PyQt6.QtGui import QPixmap, QColor, QFont, QPainter
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from typing import List, Dict, Optional
from models import Part
from utils.platform import open_url_crossplatform
from utils.algorithms import mergesort


SORT_OPTIONS = [
    ("По умолчанию",         None,        None),
    ("Цена: по возрастанию", "price",     False),
    ("Цена: по убыванию",    "price",     True),
    ("Название: А → Я",      "part_name", False),
    ("Название: Я → А",      "part_name", True),
    ("Марка: А → Я",         "brand",     False),
    ("Новинки",              "id",        True),
]

CARD_W   = 220
CARD_IMG = (220, 160)
COLS     = 4
BATCH    = 20


def make_cover_pixmap(pix: QPixmap, target_size: QSize) -> QPixmap:
    """Масштабирует pix с сохранением пропорций и обрезает до target_size (Cover)."""
    if pix.isNull():
        return pix
    scaled = pix.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation)
    x = (scaled.width() - target_size.width()) // 2
    y = (scaled.height() - target_size.height()) // 2
    return scaled.copy(x, y, target_size.width(), target_size.height())


def _placeholder(w: int, h: int, dark: bool) -> QPixmap:
    pix = QPixmap(w, h)
    pix.fill(QColor('#2a2b30' if dark else '#f1f3f5'))
    p = QPainter(pix)
    p.setPen(QColor('#5c5f66' if dark else '#adb5bd'))
    f = QFont(); f.setPointSize(28); p.setFont(f)
    p.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, '📷')
    p.end()
    return pix


class ImageCache(QObject):
    _ready = pyqtSignal(str, QPixmap)

    def __init__(self):
        super().__init__()
        self._manager  = QNetworkAccessManager()
        self._cache:   Dict[str, QPixmap]       = {}
        self._pending: Dict[str, List[QLabel]]  = {}
        self._in_flight: Dict[object, str]      = {}
        self._manager.finished.connect(self._on_finished)

    def request(self, url: str, label: QLabel) -> None:
        if url in self._cache:
            self._apply(label, self._cache[url])
            return
        if url in self._pending:
            self._pending[url].append(label)
            return
        self._pending[url] = [label]
        req   = QNetworkRequest(QUrl(url))
        reply = self._manager.get(req)
        self._in_flight[id(reply)] = url
        reply.finished.connect(lambda r=reply: self._on_finished(r))

    def _on_finished(self, reply: QNetworkReply) -> None:
        url = self._in_flight.pop(id(reply), None)
        if url is None:
            reply.deleteLater()
            return
        pix = QPixmap()
        if reply.error() == QNetworkReply.NetworkError.NoError:
            pix.loadFromData(reply.readAll())
        reply.deleteLater()

        if pix.isNull():
            self._pending.pop(url, None)
            return

        target_size = QSize(*CARD_IMG)
        scaled_cover = make_cover_pixmap(pix, target_size)
        self._cache[url] = scaled_cover

        for label in self._pending.pop(url, []):
            if not sip.isdeleted(label):
                self._apply(label, scaled_cover)

    @staticmethod
    def _apply(label: QLabel, pix: QPixmap) -> None:
        if not sip.isdeleted(label):
            label.setPixmap(pix)

    def clear(self) -> None:
        self._cache.clear()

    def get(self, url: str) -> Optional[QPixmap]:
        return self._cache.get(url)


_image_cache = ImageCache()


def get_image_cache() -> ImageCache:
    return _image_cache


class PartCard(QFrame):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, part: Part, dark: bool = False, parent=None):
        super().__init__(parent)
        self.part = part
        self.dark = dark
        self._build()
        self._style()

    def _build(self):
        self.setFixedWidth(CARD_W)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 12)
        root.setSpacing(0)

        self.imgLabel = QLabel(self)
        self.imgLabel.setFixedSize(*CARD_IMG)
        self.imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imgLabel.setScaledContents(False)

        url = self.part.photo_url
        cache = get_image_cache()
        if url:
            cached = cache.get(url)
            if cached:
                self.imgLabel.setPixmap(cached)
            else:
                self.imgLabel.setPixmap(_placeholder(*CARD_IMG, self.dark))
                cache.request(url, self.imgLabel)
        else:
            self.imgLabel.setPixmap(_placeholder(*CARD_IMG, self.dark))

        root.addWidget(self.imgLabel)

        body = QVBoxLayout()
        body.setContentsMargins(12, 10, 12, 0)
        body.setSpacing(4)

        cond_color = '#2f9e44' if self.part.condition == 'new' else '#e67700'
        badge = QLabel('NEW' if self.part.condition == 'new' else 'USED')
        badge.setFixedWidth(46)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background-color:{cond_color};color:white;"
            f"border-radius:4px;padding:2px 0;font-size:10px;font-weight:700;"
        )

        lbl_name = QLabel(self.part.part_name or '')
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("font-weight:700;font-size:13px;")

        lbl_oem = QLabel(f"OEM: {self.part.oem_number}")
        lbl_oem.setStyleSheet("font-size:11px;color:#868e96;")

        lbl_car = QLabel(self.part.car_info)
        lbl_car.setWordWrap(True)
        lbl_car.setStyleSheet("font-size:11px;")

        lbl_price = QLabel(f"{self.part.price:,.0f} ₸")
        lbl_price.setStyleSheet(
            "font-size:16px;font-weight:700;color:#e67700;margin-top:4px;"
        )

        qty_color = '#2f9e44' if self.part.quantity > 0 else '#fa5252'
        qty_text  = (f"В наличии: {self.part.quantity}"
                     if self.part.quantity > 0 else "Нет в наличии")
        lbl_qty = QLabel(qty_text)
        lbl_qty.setStyleSheet(f"font-size:11px;color:{qty_color};")

        body.addWidget(badge)
        body.addSpacing(4)
        body.addWidget(lbl_name)
        body.addWidget(lbl_oem)
        body.addWidget(lbl_car)

        if self.part.year_start or self.part.year_end:
            lbl_years = QLabel(f"📅 {self.part.years_display}")
            lbl_years.setStyleSheet("font-size:11px;color:#868e96;")
            body.addWidget(lbl_years)

        body.addWidget(lbl_price)
        body.addWidget(lbl_qty)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)
        btn_row.setContentsMargins(0, 8, 0, 0)

        if self.part.shop_url:
            shop_btn = QPushButton("🔗 Магазин")
            shop_btn.setProperty("cardBtn", True)
            shop_btn.clicked.connect(lambda: open_url_crossplatform(self.part.shop_url))
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

    def _style(self):
        if self.dark:
            self.setStyleSheet(
                "PartCard{background-color:#25262b;border:1px solid #373a40;"
                "border-radius:10px;}"
                "PartCard:hover{border:1px solid #1c7ed6;}"
                "QPushButton[cardBtn=true]{padding:5px 10px;font-size:11px;}"
            )
        else:
            self.setStyleSheet(
                "PartCard{background-color:#ffffff;border:1px solid #e9ecef;"
                "border-radius:10px;}"
                "PartCard:hover{border:1px solid #339af0;}"
                "QPushButton[cardBtn=true]{padding:5px 10px;font-size:11px;}"
            )


class CardView(QWidget):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parts:  List[Part] = []
        self._sorted: List[Part] = []
        self._dark    = False
        self._rendered = 0
        self._batch_timer = QTimer(self)
        self._batch_timer.setSingleShot(True)
        self._batch_timer.timeout.connect(self._render_next_batch)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        lbl = QLabel("Сортировка:")
        lbl.setStyleSheet("font-size:13px;")

        self.sortCombo = QComboBox()
        self.sortCombo.setMinimumWidth(200)
        for label, _, _ in SORT_OPTIONS:
            self.sortCombo.addItem(label)
        self.sortCombo.currentIndexChanged.connect(self._on_sort_changed)

        self.countLabel = QLabel("")
        self.countLabel.setStyleSheet("color:#868e96;font-size:12px;")

        toolbar.addWidget(lbl)
        toolbar.addWidget(self.sortCombo)
        toolbar.addStretch()
        toolbar.addWidget(self.countLabel)
        root.addLayout(toolbar)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        self._container = QWidget()
        self._grid = QGridLayout(self._container)
        self._grid.setSpacing(16)
        self._grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self._scroll.setWidget(self._container)
        root.addWidget(self._scroll)

    def set_dark(self, dark: bool):
        self._dark = dark
        self._full_rerender()

    def set_parts(self, parts: List[Part]):
        self._parts = parts
        self._on_sort_changed()

    def clear_image_cache(self):
        get_image_cache().clear()
        self._full_rerender()

    def _on_sort_changed(self):
        idx = self.sortCombo.currentIndex()
        _, key, reverse = SORT_OPTIONS[idx]
        if not key:
            self._sorted = list(self._parts)
        else:
            def _key(p):
                v = getattr(p, key)
                if v is None:
                    return (2, '')
                if isinstance(v, (int, float)) or hasattr(v, '__float__'):
                    try:
                        return (0, float(v))
                    except Exception:
                        pass
                return (1, str(v).lower())

            self._sorted = mergesort(list(self._parts), _key, reverse=bool(reverse))

        self._start_render()

    def _start_render(self):
        self._batch_timer.stop()
        self._clear_grid()
        self._rendered = 0
        self.countLabel.setText(f"Найдено: {len(self._sorted)}")
        self._render_next_batch()

    def _render_next_batch(self):
        end = min(self._rendered + BATCH, len(self._sorted))
        for i in range(self._rendered, end):
            card = PartCard(self._sorted[i], self._dark)
            card.edit_requested.connect(self.edit_requested)
            card.delete_requested.connect(self.delete_requested)
            self._grid.addWidget(card, i // COLS, i % COLS)
        self._rendered = end
        if self._rendered < len(self._sorted):
            self._batch_timer.start(0)

    def _clear_grid(self):
        while self._grid.count():
            item = self._grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _full_rerender(self):
        self._start_render()

    def refresh(self):
        self._full_rerender()