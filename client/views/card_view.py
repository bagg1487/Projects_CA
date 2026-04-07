from PyQt5 import sip
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QScrollArea, QFrame,
    QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject, QTimer, QRect, QThread
from PyQt5.QtGui import QPixmap, QColor, QFont, QPainter, QPainterPath
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from typing import List, Dict, Optional
from models import Part
from utils.platform import open_url_crossplatform
from utils.algorithms import mergesort
from utils.image_disk_cache import (
    load_from_disk, save_to_disk, make_rounded, clear_disk_cache, RADIUS
)


SORT_OPTIONS = [
    ("По умолчанию",         None,        None),
    ("Цена: по возрастанию", "price",     False),
    ("Цена: по убыванию",    "price",     True),
    ("Название: А → Я",      "part_name", False),
    ("Название: Я → А",      "part_name", True),
    ("Марка: А → Я",         "brand",     False),
    ("Новинки",              "id",        True),
]

CARD_MIN_W   = 180
CARD_MAX_W   = 280
CARD_SPACING = 16
IMG_RATIO    = 0.72
BATCH        = 24


def _placeholder(w: int, h: int, radius: int, dark: bool) -> QPixmap:
    result = QPixmap(w, h)
    result.fill(Qt.GlobalColor.transparent)
    p = QPainter(result)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, w, h, radius, radius)
    p.setClipPath(path)
    p.fillRect(0, 0, w, h, QColor('#2a2b30' if dark else '#f1f3f5'))
    p.setPen(QColor('#5c5f66' if dark else '#adb5bd'))
    f = QFont(); f.setPointSize(28); p.setFont(f)
    p.drawText(QRect(0, 0, w, h), Qt.AlignmentFlag.AlignCenter, '📷')
    p.end()
    return result


def _apply(label: QLabel, pix: QPixmap) -> None:
    if not sip.isdeleted(label):
        label.setPixmap(pix)


class _DiskLoader(QThread):
    done = pyqtSignal(str, int, int, object)

    def __init__(self, url: str, w: int, h: int, raw: QPixmap):
        super().__init__()
        self._url = url
        self._w   = w
        self._h   = h
        self._raw = raw

    def run(self):
        rounded = make_rounded(self._raw, self._w, self._h, RADIUS)
        save_to_disk(self._url, self._w, self._h, rounded)
        self.done.emit(self._url, self._w, self._h, rounded)


class ImageCache(QObject):
    def __init__(self):
        super().__init__()
        self._manager    = QNetworkAccessManager()
        self._mem:       Dict[str, QPixmap] = {}
        self._pending:   Dict[str, list]    = {}
        self._in_flight: Dict[int, tuple]   = {}
        self._workers:   List[_DiskLoader]  = []
        self._manager.finished.connect(self._on_net_finished)

    def _mem_key(self, url: str, w: int, h: int) -> str:
        return f"{url}|{w}x{h}"

    def request(self, url: str, label: QLabel, w: int, h: int) -> None:
        key = self._mem_key(url, w, h)

        if key in self._mem:
            _apply(label, self._mem[key])
            return

        disk = load_from_disk(url, w, h)
        if disk is not None:
            self._mem[key] = disk
            _apply(label, disk)
            return

        if key in self._pending:
            self._pending[key].append(label)
            return

        self._pending[key] = [label]
        req   = QNetworkRequest(QUrl(url))
        reply = self._manager.get(req)
        self._in_flight[id(reply)] = (url, w, h)
        reply.finished.connect(lambda r=reply: self._on_net_finished(r))

    def _on_net_finished(self, reply: QNetworkReply) -> None:
        info = self._in_flight.pop(id(reply), None)
        if info is None:
            reply.deleteLater()
            return

        url, w, h = info
        key = self._mem_key(url, w, h)
        raw = QPixmap()
        if reply.error() == QNetworkReply.NetworkError.NoError:
            raw.loadFromData(reply.readAll())
        reply.deleteLater()

        if raw.isNull():
            self._pending.pop(key, None)
            return

        worker = _DiskLoader(url, w, h, raw)
        worker.done.connect(self._on_disk_saved)
        self._workers.append(worker)
        worker.start()

        rounded = make_rounded(raw, w, h, RADIUS)
        self._mem[key] = rounded

        for label in self._pending.pop(key, []):
            _apply(label, rounded)

    def _on_disk_saved(self, url: str, w: int, h: int, pix: QPixmap) -> None:
        key = self._mem_key(url, w, h)
        self._mem[key] = pix
        self._workers = [t for t in self._workers if t.isRunning()]

    def prefetch(self, url: str, w: int, h: int) -> Optional[QPixmap]:
        key = self._mem_key(url, w, h)
        if key in self._mem:
            return self._mem[key]
        disk = load_from_disk(url, w, h)
        if disk is not None:
            self._mem[key] = disk
            return disk
        return None

    def clear_mem(self) -> None:
        self._mem.clear()

    def clear_all(self) -> int:
        self._mem.clear()
        return clear_disk_cache()


_image_cache = ImageCache()


def get_image_cache() -> ImageCache:
    return _image_cache


class PartCard(QFrame):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, part: Part, card_w: int, dark: bool = False, parent=None):
        super().__init__(parent)
        self.part   = part
        self.dark   = dark
        self.card_w = card_w
        self.img_h  = int(card_w * IMG_RATIO)
        self._build()
        self._style()

    def _build(self):
        self.setFixedWidth(self.card_w)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 12)
        root.setSpacing(0)

        self.imgLabel = QLabel(self)
        self.imgLabel.setFixedSize(self.card_w, self.img_h)
        self.imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imgLabel.setScaledContents(False)

        url   = self.part.photo_url
        cache = get_image_cache()
        if url:
            cached = cache.prefetch(url, self.card_w, self.img_h)
            if cached:
                self.imgLabel.setPixmap(cached)
            else:
                self.imgLabel.setPixmap(_placeholder(self.card_w, self.img_h, RADIUS, self.dark))
                cache.request(url, self.imgLabel, self.card_w, self.img_h)
        else:
            self.imgLabel.setPixmap(_placeholder(self.card_w, self.img_h, RADIUS, self.dark))

        root.addWidget(self.imgLabel)

        body = QVBoxLayout()
        body.setContentsMargins(10, 8, 10, 0)
        body.setSpacing(3)

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
            "font-size:15px;font-weight:700;color:#e67700;margin-top:4px;"
        )

        qty_color = '#2f9e44' if self.part.quantity > 0 else '#fa5252'
        qty_text  = (f"В наличии: {self.part.quantity}"
                     if self.part.quantity > 0 else "Нет в наличии")
        lbl_qty = QLabel(qty_text)
        lbl_qty.setStyleSheet(f"font-size:11px;color:{qty_color};")

        body.addWidget(badge)
        body.addSpacing(3)
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
        btn_row.setContentsMargins(0, 6, 0, 0)

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
        r = RADIUS
        if self.dark:
            self.setStyleSheet(
                f"PartCard{{background-color:#25262b;border:1px solid #373a40;border-radius:{r}px;}}"
                f"PartCard:hover{{border:1px solid #1c7ed6;}}"
                "QPushButton[cardBtn=true]{padding:5px 8px;font-size:11px;}"
            )
        else:
            self.setStyleSheet(
                f"PartCard{{background-color:#ffffff;border:1px solid #e9ecef;border-radius:{r}px;}}"
                f"PartCard:hover{{border:1px solid #339af0;}}"
                "QPushButton[cardBtn=true]{padding:5px 8px;font-size:11px;}"
            )


class CardView(QWidget):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parts:   List[Part] = []
        self._sorted:  List[Part] = []
        self._dark     = False
        self._rendered = 0
        self._cols     = 4
        self._card_w   = 220

        self._batch_timer = QTimer(self)
        self._batch_timer.setSingleShot(True)
        self._batch_timer.timeout.connect(self._render_next_batch)

        self._resize_timer = QTimer(self)
        self._resize_timer.setSingleShot(True)
        self._resize_timer.setInterval(120)
        self._resize_timer.timeout.connect(self._on_resize_settled)

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
        self._grid.setSpacing(CARD_SPACING)
        self._grid.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self._scroll.setWidget(self._container)
        root.addWidget(self._scroll)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_timer.start()

    def _on_resize_settled(self):
        cols, card_w = self._compute_layout()
        if cols != self._cols or card_w != self._card_w:
            self._cols   = cols
            self._card_w = card_w
            self._start_render()

    def _compute_layout(self):
        available = self._scroll.viewport().width() - 4
        if available < CARD_MIN_W:
            available = self.width() - 20
        cols     = max(1, available // (CARD_MIN_W + CARD_SPACING))
        spacing  = CARD_SPACING * (cols - 1)
        card_w   = (available - spacing) // cols
        card_w   = max(CARD_MIN_W, min(CARD_MAX_W, card_w))
        return cols, card_w

    def set_dark(self, dark: bool):
        self._dark = dark
        self._start_render()

    def set_parts(self, parts: List[Part]):
        self._parts = parts
        self._on_sort_changed()

    def clear_image_cache(self):
        get_image_cache().clear_mem()
        self._start_render()

    def clear_all_cache(self) -> int:
        n = get_image_cache().clear_all()
        self._start_render()
        return n

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

        self._cols, self._card_w = self._compute_layout()
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
            card = PartCard(self._sorted[i], self._card_w, self._dark)
            card.edit_requested.connect(self.edit_requested)
            card.delete_requested.connect(self.delete_requested)
            self._grid.addWidget(card, i // self._cols, i % self._cols)
        self._rendered = end
        if self._rendered < len(self._sorted):
            self._batch_timer.start(0)

    def _clear_grid(self):
        while self._grid.count():
            item = self._grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def refresh(self):
        self._start_render()