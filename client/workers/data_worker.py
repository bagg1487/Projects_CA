from PyQt5.QtCore import QThread, pyqtSignal
from typing import List, Optional
from models import Part, InventoryItem
from controllers.part_controller import PartController

class DataLoadWorker(QThread):
    finished = pyqtSignal(list, list)
    error = pyqtSignal(str)

    def __init__(self, controller: PartController, filters: dict):
        super().__init__()
        self.controller = controller
        self.filters = filters

    def run(self):
        try:
            parts = self.controller.get_all_parts(
                search=self.filters.get('search', ''),
                brand=self.filters.get('brand', ''),
                condition=self.filters.get('condition', ''),
                location=self.filters.get('location', ''),
                in_stock_only=self.filters.get('in_stock_only', False)
            )
            inventory = self.controller.get_inventory()
            self.finished.emit(parts, inventory)
        except Exception as e:
            self.error.emit(str(e))