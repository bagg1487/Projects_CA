from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import List
from models import Part
from controllers.part_controller import PartController
from views.dialogs import PartDialog
from utils.theme import ThemeManager


class MainWindow(QMainWindow):
    """Главное окно приложения (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = PartController()
        self.theme_manager = ThemeManager()
        self.isDarkMode = False

        self.setupUI()
        self.setupModels()
        self.connectSignals()
        self.loadFilters()
        self.refreshData()
        self.applyLightTheme()

        self.resize(1024, 768)
        self.setWindowTitle("Система складского учета автозапчастей")

    def setupUI(self):
        """Настройка UI компонентов"""
        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setSpacing(15)
        mainLayout.setContentsMargins(20, 20, 20, 20)

        # Верхняя панель с фильтрами
        topPanel = self.createFilterPanel()

        # Панель с кнопками действий
        buttonPanel = self.createButtonPanel()

        # Табы с таблицами
        self.tabWidget = QTabWidget(self)
        self.setupCatalogTab()
        self.setupInventoryTab()

        mainLayout.addLayout(topPanel)
        mainLayout.addLayout(buttonPanel)
        mainLayout.addWidget(self.tabWidget)

        self.setCentralWidget(centralWidget)

    def createFilterPanel(self) -> QHBoxLayout:
        """Создать панель фильтров"""
        layout = QHBoxLayout()
        layout.setSpacing(10)

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

        layout.addWidget(self.searchEdit)
        layout.addWidget(self.brandFilter)
        layout.addWidget(self.conditionFilter)
        layout.addWidget(self.locationFilter)
        layout.addWidget(self.inStockCheckbox)
        layout.addStretch()
        layout.addWidget(self.themeToggleBtn)

        return layout

    def createButtonPanel(self) -> QHBoxLayout:
        """Создать панель кнопок"""
        layout = QHBoxLayout()

        self.addBtn = QPushButton("Добавить деталь", self)
        self.editBtn = QPushButton("Редактировать", self)
        self.deleteBtn = QPushButton("Удалить", self)
        self.deleteBtn.setObjectName("deleteBtn")

        layout.addWidget(self.addBtn)
        layout.addWidget(self.editBtn)
        layout.addWidget(self.deleteBtn)
        layout.addStretch()

        return layout

    def setupCatalogTab(self):
        """Настройка вкладки каталога"""
        catalogTab = QWidget()
        catalogLayout = QVBoxLayout(catalogTab)

        self.catalogTable = QTableView(self)
        self.catalogTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.catalogTable.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.catalogTable.horizontalHeader().setStretchLastSection(True)

        catalogLayout.addWidget(self.catalogTable)
        self.tabWidget.addTab(catalogTab, "Каталог запчастей")

    def setupInventoryTab(self):
        """Настройка вкладки инвентаря"""
        inventoryTab = QWidget()
        inventoryLayout = QVBoxLayout(inventoryTab)

        self.inventoryTable = QTableView(self)
        self.inventoryTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.inventoryTable.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.inventoryTable.horizontalHeader().setStretchLastSection(True)

        inventoryLayout.addWidget(self.inventoryTable)
        self.tabWidget.addTab(inventoryTab, "Наличие по складам")

    def setupModels(self):
        """Настройка моделей данных для таблиц"""
        # Модель для каталога
        self.catalogModel = QStandardItemModel(0, 4, self)
        self.catalogModel.setHorizontalHeaderLabels(
            ["ID", "OEM-номер", "Наименование", "Марка/Модель"]
        )
        self.catalogTable.setModel(self.catalogModel)

        # Модель для инвентаря
        self.inventoryModel = QStandardItemModel(0, 6, self)
        self.inventoryModel.setHorizontalHeaderLabels(
            ["Деталь", "OEM", "Марка/Модель", "Цена", "Количество", "Адрес склада"]
        )
        self.inventoryTable.setModel(self.inventoryModel)

        # Скрываем колонку ID
        self.catalogTable.setColumnHidden(0, True)

    def connectSignals(self):
        """Подключение сигналов"""
        self.searchEdit.textChanged.connect(self.refreshData)
        self.brandFilter.currentTextChanged.connect(self.refreshData)
        self.conditionFilter.currentTextChanged.connect(self.refreshData)
        self.locationFilter.currentTextChanged.connect(self.refreshData)
        self.inStockCheckbox.stateChanged.connect(self.refreshData)
        self.themeToggleBtn.clicked.connect(self.toggleTheme)

        self.addBtn.clicked.connect(self.addPart)
        self.editBtn.clicked.connect(self.editPart)
        self.deleteBtn.clicked.connect(self.deletePart)

    def loadFilters(self):
        """Загрузка фильтров"""
        try:
            brands = self.controller.get_brands()
            self.brandFilter.addItems(brands)

            locations = self.controller.get_locations()
            self.locationFilter.addItems(locations)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить фильтры: {e}")

    def refreshData(self):
        """Обновление данных в таблицах"""
        self.loadCatalogData()
        self.loadInventoryData()

    def loadCatalogData(self):
        """Загрузка данных каталога"""
        try:
            parts = self.controller.get_all_parts(
                search=self.searchEdit.text(),
                brand=self.brandFilter.currentText(),
                condition=self.conditionFilter.currentText(),
                location=self.locationFilter.currentText(),
                in_stock_only=self.inStockCheckbox.isChecked()
            )

            self.catalogModel.setRowCount(0)
            for part in parts:
                row = self.catalogModel.rowCount()
                self.catalogModel.insertRow(row)

                self.catalogModel.setItem(row, 0, QStandardItem(str(part.id)))
                self.catalogModel.setItem(row, 1, QStandardItem(part.oem_number))
                self.catalogModel.setItem(row, 2, QStandardItem(part.part_name))
                self.catalogModel.setItem(row, 3, QStandardItem(part.car_info))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {e}")

    def loadInventoryData(self):
        """Загрузка данных инвентаря"""
        try:
            inventory = self.controller.get_inventory()

            self.inventoryModel.setRowCount(0)
            for item in inventory:
                row = self.inventoryModel.rowCount()
                self.inventoryModel.insertRow(row)

                self.inventoryModel.setItem(row, 0, QStandardItem(item.part_name))
                self.inventoryModel.setItem(row, 1, QStandardItem(item.oem_number))
                self.inventoryModel.setItem(row, 2, QStandardItem(item.car_model))
                self.inventoryModel.setItem(row, 3, QStandardItem(str(item.price)))
                self.inventoryModel.setItem(row, 4, QStandardItem(str(item.quantity)))
                self.inventoryModel.setItem(row, 5, QStandardItem(item.address))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить инвентарь: {e}")

    def addPart(self):
        """Добавление запчасти"""
        dialog = PartDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.getData()
                self.controller.add_part(data)
                self.refreshData()
                QMessageBox.information(self, "Успех", "Запчасть добавлена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def editPart(self):
        """Редактирование запчасти"""
        selected = self.catalogTable.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для редактирования")
            return

        row = selected[0].row()
        part_id = int(self.catalogModel.item(row, 0).text())
        part = self.controller.get_part(part_id)

        if not part:
            QMessageBox.warning(self, "Ошибка", "Запчасть не найдена")
            return

        dialog = PartDialog(self, part)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.getData()
                self.controller.update_part(part_id, data)
                self.refreshData()
                QMessageBox.information(self, "Успех", "Запчасть обновлена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def deletePart(self):
        """Удаление запчасти"""
        selected = self.catalogTable.selectedIndexes()
        if not selected:
            QMessageBox.warning(self, "Предупреждение", "Выберите запчасть для удаления")
            return

        row = selected[0].row()
        part_id = int(self.catalogModel.item(row, 0).text())
        part_name = self.catalogModel.item(row, 2).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить запчасть '{part_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.controller.delete_part(part_id):
                    self.refreshData()
                    QMessageBox.information(self, "Успех", "Запчасть удалена")
                else:
                    QMessageBox.warning(self, "Ошибка", "Запчасть не найдена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def toggleTheme(self):
        """Переключение темы"""
        self.isDarkMode = not self.isDarkMode
        if self.isDarkMode:
            self.themeToggleBtn.setText("☀️ Светлая тема")
            self.applyDarkTheme()
        else:
            self.themeToggleBtn.setText("🌙 Тёмная тема")
            self.applyLightTheme()

    def applyLightTheme(self):
        """Применить светлую тему"""
        self.setStyleSheet(self.theme_manager.light_theme())

    def applyDarkTheme(self):
        """Применить тёмную тему"""
        self.setStyleSheet(self.theme_manager.dark_theme())