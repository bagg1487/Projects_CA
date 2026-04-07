from PyQt5.QtCore import QThread, pyqtSignal
from controllers.part_controller import PartController
from utils.drom_parser import DromParser
import traceback

class UpdateWorker(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, controller: PartController):
        super().__init__()
        self.controller = controller
        self.parser = DromParser(delay=0.5)

    def run(self):
        try:
            all_parts = self.controller.get_all_parts()
            missing = [p for p in all_parts if not p.photo_url or not p.shop_url]
            total = len(missing)
            for i, part in enumerate(missing):
                self.progress.emit(i+1, total)
                photo, shop = self.parser.get_image_and_shop_url(part.part_name)
                if photo or shop:
                    update_data = {}
                    if photo:
                        update_data['photo_url'] = photo
                    if shop:
                        update_data['shop_url'] = shop
                    self.controller.update_part_fields(part.id, update_data)
            self.finished.emit()
        except Exception as e:
            self.error.emit(traceback.format_exc())