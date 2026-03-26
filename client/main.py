import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from database import Database

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isDarkMode = False
        self.db = Database()

        self.setupUI()
        self.setupModels()
        self.applyLightTheme()
        self.connectSignals()

        self.resize(1200, 800)
        self.setWindowTitle("Система складского учета автозапчастей")
        
        self.loadFilters()
        self.refreshInventory()

    def setupUI(self):
        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setSpacing(15)
        mainLayout.setContentsMargins(20, 20, 20, 20)

        # Верхняя панель
        topPanelLayout = QHBoxLayout()
        topPanelLayout.setSpacing(10)

        self.searchEdit = QLineEdit(self)
        self.searchEdit.setPlaceholderText("Поиск по OEM, названию или марке/модели...")
        self.searchEdit.setMinimumWidth(300)

        self.brandFilter = QComboBox(self)
        self.brandFilter.addItem("Все марки")

        self.conditionFilter = QComboBox(self)
        self.conditionFilter.addItem("Любое состояние")
        self.conditionFilter.addItem("NEW")
        self.conditionFilter.addItem("USED")

        self.locationFilter = QComboBox(self)
        self.locationFilter.addItem("Все склады")

        self.inStockCheckbox = QCheckBox("Только в наличии", self)

        self.themeToggleBtn = QPushButton("🌙 Тёмная тема", self)
        self.themeToggleBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        topPanelLayout.addWidget(self.searchEdit)
        topPanelLayout.addWidget(self.brandFilter)
        topPanelLayout.addWidget(self.conditionFilter)
        topPanelLayout.addWidget(self.locationFilter)
        topPanelLayout.addWidget(self.inStockCheckbox)
        topPanelLayout.addStretch()
        topPanelLayout.addWidget(self.themeToggleBtn)

        # Кнопки действий
        buttonLayout = QHBoxLayout()
        self.addBtn = QPushButton("Добавить деталь", self)
        self.editBtn = QPushButton("Редактировать", self)
        self.deleteBtn = QPushButton("Удалить", self)
        self.deleteBtn.setObjectName("deleteBtn")
        self.refreshBtn = QPushButton("Обновить", self)

        buttonLayout.addWidget(self.addBtn)
        buttonLayout.addWidget(self.editBtn)
        buttonLayout.addWidget(self.deleteBtn)
        buttonLayout.addWidget(self.refreshBtn)
        buttonLayout.addStretch()

        # Табы
        self.tabWidget = QTabWidget(self)

        catalogTab = QWidget()
        catalogLayout = QVBoxLayout(catalogTab)
        self.catalogTable = QTableView(self)
        self.catalogTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.catalogTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.catalogTable.horizontalHeader().setStretchLastSection(True)
        catalogLayout.addWidget(self.catalogTable)

        inventoryTab = QWidget()
        inventoryLayout = QVBoxLayout(inventoryTab)
        self.inventoryTable = QTableView(self)
        self.inventoryTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventoryTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.inventoryTable.horizontalHeader().setStretchLastSection(True)
        inventoryLayout.addWidget(self.inventoryTable)

        self.tabWidget.addTab(catalogTab, "Каталог запчастей")
        self.tabWidget.addTab(inventoryTab, "Наличие по складам")

        mainLayout.addLayout(topPanelLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.tabWidget)

        self.setCentralWidget(centralWidget)

    def setupModels(self):
        # Каталог: OEM, Наименование, Марка/Модель, Годы, Фото, Ссылка
        catalogModel = QStandardItemModel(0, 6, self)
        catalogModel.setHorizontalHeaderLabels([
            "OEM-номер", "Наименование", "Марка", "Модель", "Годы", "Фото", "Ссылка"
        ])
        self.catalogTable.setModel(catalogModel)

        # Инвентарь: OEM, Деталь, Марка/Модель, Цена, Кол-во, Состояние, Магазин, Адрес, Телефон, Ссылка
        inventoryModel = QStandardItemModel(0, 10, self)
        inventoryModel.setHorizontalHeaderLabels([
            "OEM", "Деталь", "Марка", "Модель", "Цена", "Количество", 
            "Состояние", "Магазин", "Адрес", "Ссылка"
        ])
        self.inventoryTable.setModel(inventoryModel)

    def connectSignals(self):
        self.themeToggleBtn.clicked.connect(self.toggleTheme)
        self.addBtn.clicked.connect(self.addPart)
        self.editBtn.clicked.connect(self.editPart)
        self.deleteBtn.clicked.connect(self.deletePart)
        self.refreshBtn.clicked.connect(self.refreshInventory)
        self.searchEdit.textChanged.connect(self.applyFilters)
        self.brandFilter.currentTextChanged.connect(self.applyFilters)
        self.conditionFilter.currentTextChanged.connect(self.applyFilters)
        self.locationFilter.currentTextChanged.connect(self.applyFilters)
        self.inStockCheckbox.stateChanged.connect(self.applyFilters)

    def toggleTheme(self):
        self.isDarkMode = not self.isDarkMode
        if self.isDarkMode:
            self.themeToggleBtn.setText("☀️ Светлая тема")
            self.applyDarkTheme()
        else:
            self.themeToggleBtn.setText("🌙 Тёмная тема")
            self.applyLightTheme()

    def applyLightTheme(self):
        styleSheet = """
        QMainWindow { background-color: #f4f6f9; color: #212529; }
        QWidget { color: #212529; }
        QLineEdit, QComboBox, QSpinBox {
            padding: 8px 12px; border: 1px solid #ced4da; border-radius: 6px;
            background-color: #ffffff; color: #212529; font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #4dabf7; }
        QPushButton {
            padding: 8px 16px; background-color: #339af0; color: white;
            border: none; border-radius: 6px; font-size: 14px; font-weight: bold;
        }
        QPushButton:hover { background-color: #228be6; }
        QPushButton#deleteBtn { background-color: #fa5252; }
        QPushButton#deleteBtn:hover { background-color: #f03e3e; }
        QTableView {
            background-color: #ffffff; border: 1px solid #e9ecef; border-radius: 6px;
            gridline-color: #f1f3f5; selection-background-color: #e7f5ff; selection-color: #212529;
        }
        QHeaderView::section {
            background-color: #f8f9fa; padding: 8px; border: none;
            border-bottom: 2px solid #dee2e6; font-weight: bold; color: #495057;
        }
        QTabWidget::pane { border: 1px solid #dee2e6; border-radius: 6px; background-color: #ffffff; }
        QTabBar::tab {
            background: #e9ecef; padding: 10px 20px; margin-right: 2px;
            border-top-left-radius: 6px; border-top-right-radius: 6px; color: #495057;
        }
        QTabBar::tab:selected {
            background: #ffffff; border: 1px solid #dee2e6; border-bottom-color: #ffffff;
            font-weight: bold; color: #212529;
        }
        """
        self.setStyleSheet(styleSheet)

    def applyDarkTheme(self):
        styleSheet = """
        QMainWindow { background-color: #121212; color: #e0e0e0; }
        QWidget { color: #e0e0e0; }
        QLineEdit, QComboBox, QSpinBox {
            padding: 8px 12px; border: 1px solid #333333; border-radius: 6px;
            background-color: #1e1e1e; color: #e0e0e0; font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #339af0; }
        QComboBox QAbstractItemView {
            background-color: #1e1e1e; color: #e0e0e0; selection-background-color: #339af0;
        }
        QPushButton {
            padding: 8px 16px; background-color: #339af0; color: white;
            border: none; border-radius: 6px; font-size: 14px; font-weight: bold;
        }
        QPushButton:hover { background-color: #228be6; }
        QPushButton#deleteBtn { background-color: #e03131; }
        QPushButton#deleteBtn:hover { background-color: #c92a2a; }
        QTableView {
            background-color: #1e1e1e; border: 1px solid #333333; border-radius: 6px;
            gridline-color: #2c2c2c; selection-background-color: #2b4f73; selection-color: #ffffff;
        }
        QHeaderView::section {
            background-color: #252526; padding: 8px; border: none;
            border-bottom: 2px solid #333333; font-weight: bold; color: #b0b0b0;
        }
        QTabWidget::pane { border: 1px solid #333333; border-radius: 6px; background-color: #1e1e1e; }
        QTabBar::tab {
            background: #252526; padding: 10px 20px; margin-right: 2px;
            border-top-left-radius: 6px; border-top-right-radius: 6px; color: #b0b0b0;
        }
        QTabBar::tab:selected {
            background: #1e1e1e; border: 1px solid #333333; border-bottom-color: #1e1e1e;
            font-weight: bold; color: #e0e0e0;
        }
        """
        self.setStyleSheet(styleSheet)

    def loadFilters(self):
        """Загрузить фильтры из БД"""
        brands = self.db.get_all_brands()
        for brand in brands:
            self.brandFilter.addItem(brand)

        locations = self.db.get_all_locations()
        for store_name, address in locations:
            display = f"{store_name} ({address})" if address else store_name
            self.locationFilter.addItem(display)

    def refreshInventory(self):
        """Обновить данные в таблицах"""
        self.applyFilters()

    def applyFilters(self):
        """Применить фильтры и обновить таблицы"""
        search = self.searchEdit.text()
        brand = self.brandFilter.currentText()
        if brand == "Все марки":
            brand = ""
        condition = self.conditionFilter.currentText()
        location = self.locationFilter.currentText()
        if location == "Все склады":
            location = ""
        in_stock = self.inStockCheckbox.isChecked()

        parts = self.db.get_parts(
            search=search,
            brand=brand,
            condition=condition,
            location=location,
            in_stock_only=in_stock
        )

        # Обновить каталог
        catalogModel = self.catalogTable.model()
        catalogModel.setRowCount(0)
        for row in parts:
            oem, name, brand, model, body, year_start, year_end, photo, shop_url = row
            years = f"{year_start or '?'}-{year_end or '?'}" if year_start or year_end else "?"
            catalogModel.appendRow([
                QStandardItem(oem or ""),
                QStandardItem(name or ""),
                QStandardItem(brand or ""),
                QStandardItem(model or ""),
                QStandardItem(years),
                QStandardItem(photo or ""),
                QStandardItem(shop_url or "")
            ])

        # Обновить инвентарь
        inventory = self.db.get_inventory()
        inventoryModel = self.inventoryTable.model()
        inventoryModel.setRowCount(0)
        for row in inventory:
            oem, name, brand, model, body, year_start, year_end, price, qty, condition, store, address, phone, shop_url, photo = row
            inventoryModel.appendRow([
                QStandardItem(oem or ""),
                QStandardItem(name or ""),
                QStandardItem(brand or ""),
                QStandardItem(model or ""),
                QStandardItem(str(price) if price else ""),
                QStandardItem(str(qty) if qty is not None else "0"),
                QStandardItem(condition or ""),
                QStandardItem(store or ""),
                QStandardItem(address or ""),
                QStandardItem(shop_url or "")
            ])

    def addPart(self):
        """Диалог добавления запчасти"""
        dialog = PartDialog(self, db=self.db)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refreshInventory()

    def editPart(self):
        """Диалог редактирования запчасти"""
        current_tab = self.tabWidget.currentIndex()
        if current_tab == 0:
            row = self.catalogTable.currentIndex().row()
            if row < 0:
                QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для редактирования")
                return
            part_id = self.catalogTable.model().index(row, 0).data()
        else:
            row = self.inventoryTable.currentIndex().row()
            if row < 0:
                QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для редактирования")
                return
            # Для инвентаря нужен ID - упростим: поиск по OEM
            oem = self.inventoryTable.model().index(row, 0).data()
            # В реальной реализации нужно хранить ID в скрытой колонке
            QMessageBox.information(self, "Инфо", "Редактирование по ID будет реализовано")
            return

        dialog = PartDialog(self, db=self.db, part_id=part_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refreshInventory()

    def deletePart(self):
        """Удаление запчасти"""
        current_tab = self.tabWidget.currentIndex()
        if current_tab == 0:
            row = self.catalogTable.currentIndex().row()
            if row < 0:
                QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для удаления")
                return
            part_id = self.catalogTable.model().index(row, 0).data()
        else:
            row = self.inventoryTable.currentIndex().row()
            if row < 0:
                QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для удаления")
                return
            oem = self.inventoryTable.model().index(row, 0).data()
            QMessageBox.information(self, "Инфо", "Удаление по ID будет реализовано")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить запчасть ID={part_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_part(part_id)
            self.refreshInventory()


class PartDialog(QDialog):
    """Диалог добавления/редактирования запчасти"""
    def __init__(self, parent=None, db=None, part_id=None):
        super().__init__(parent)
        self.db = db
        self.part_id = part_id
        self.setWindowTitle("Редактирование запчасти" if part_id else "Добавление запчасти")
        self.resize(500, 600)
        self.setupUI()
        if part_id:
            self.loadPartData()

    def setupUI(self):
        layout = QVBoxLayout(self)
        formLayout = QFormLayout()

        self.oemEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.photoEdit = QLineEdit()
        self.brandEdit = QLineEdit()
        self.modelEdit = QLineEdit()
        self.bodyEdit = QLineEdit()
        self.yearStartEdit = QLineEdit()
        self.yearEndEdit = QLineEdit()
        self.addressEdit = QLineEdit()
        self.storeEdit = QLineEdit()
        self.phoneEdit = QLineEdit()
        self.shopUrlEdit = QLineEdit()
        self.shopUrlEdit.setPlaceholderText("https://...")
        self.qtyEdit = QSpinBox()
        self.qtyEdit.setMaximum(999999)
        self.priceEdit = QLineEdit()
        self.conditionCombo = QComboBox()
        self.conditionCombo.addItems(["NEW", "USED"])

        formLayout.addRow("OEM-номер:", self.oemEdit)
        formLayout.addRow("Название:", self.nameEdit)
        formLayout.addRow("Фото URL:", self.photoEdit)
        formLayout.addRow("Марка:", self.brandEdit)
        formLayout.addRow("Модель:", self.modelEdit)
        formLayout.addRow("Код кузова:", self.bodyEdit)
        formLayout.addRow("Год начала:", self.yearStartEdit)
        formLayout.addRow("Год окончания:", self.yearEndEdit)
        formLayout.addRow("Адрес:", self.addressEdit)
        formLayout.addRow("Магазин:", self.storeEdit)
        formLayout.addRow("Телефон:", self.phoneEdit)
        formLayout.addRow("Ссылка на магазин:", self.shopUrlEdit)
        formLayout.addRow("Количество:", self.qtyEdit)
        formLayout.addRow("Цена:", self.priceEdit)
        formLayout.addRow("Состояние:", self.conditionCombo)

        layout.addLayout(formLayout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def loadPartData(self):
        """Загрузить данные запчасти для редактирования"""
        # Упрощённая реализация
        pass

    def accept(self):
        """Сохранить данные"""
        try:
            self.db.add_part(
                oem_number=self.oemEdit.text().strip(),
                part_name=self.nameEdit.text().strip(),
                photo_url=self.photoEdit.text().strip() or None,
                brand=self.brandEdit.text().strip(),
                model=self.modelEdit.text().strip(),
                body_code=self.bodyEdit.text().strip() or None,
                year_start=int(self.yearStartEdit.text()) if self.yearStartEdit.text() else None,
                year_end=int(self.yearEndEdit.text()) if self.yearEndEdit.text() else None,
                address=self.addressEdit.text().strip(),
                store_name=self.storeEdit.text().strip(),
                phone=self.phoneEdit.text().strip() or None,
                shop_url=self.shopUrlEdit.text().strip() or '',
                quantity=self.qtyEdit.value(),
                price=float(self.priceEdit.text().replace(',', '.')),
                condition=self.conditionCombo.currentText()
            )
            QMessageBox.information(self, "Успех", "Запчасть добавлена")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
