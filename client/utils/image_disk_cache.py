import hashlib
import os
from pathlib import Path
from typing import Optional
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath


CACHE_DIR = Path(__file__).parent.parent / "cache" / "images"
RADIUS = 10


def _cache_dir() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR


def _url_to_filename(url: str, w: int, h: int) -> str:
    h_hex = hashlib.md5(url.encode()).hexdigest()
    return f"{h_hex}_{w}x{h}.png"


def load_from_disk(url: str, w: int, h: int) -> Optional[QPixmap]:
    path = _cache_dir() / _url_to_filename(url, w, h)
    if path.exists():
        pix = QPixmap(str(path))
        if not pix.isNull():
            return pix
    return None


def save_to_disk(url: str, w: int, h: int, pix: QPixmap) -> None:
    try:
        path = _cache_dir() / _url_to_filename(url, w, h)
        pix.save(str(path), "PNG")
    except Exception:
        pass


def make_rounded(pix: QPixmap, w: int, h: int, radius: int = RADIUS) -> QPixmap:
    scaled = pix.scaled(
        w, h,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation,
    )
    x = (scaled.width()  - w) // 2
    y = (scaled.height() - h) // 2
    cropped = scaled.copy(x, y, w, h)

    result = QPixmap(w, h)
    result.fill(Qt.GlobalColor.transparent)
    p = QPainter(result)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, w, h, radius, radius)
    p.setClipPath(path)
    p.drawPixmap(0, 0, cropped)
    p.end()
    return result


def clear_disk_cache() -> int:
    removed = 0
    try:
        for f in _cache_dir().glob("*.png"):
            f.unlink()
            removed += 1
    except Exception:
        pass
    return removed