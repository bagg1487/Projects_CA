import sys
import subprocess
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

def open_url_crossplatform(url: str):
    try:
        if sys.platform == 'win32':
            subprocess.run(['cmd.exe', '/C', 'start', '', url], check=True)
        elif sys.platform == 'darwin':
            subprocess.run(['open', url], check=True)
        else:
            subprocess.run(['xdg-open', url], check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        QDesktopServices.openUrl(QUrl(url))