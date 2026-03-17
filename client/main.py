import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.isDarkMode = False
        
        self.setupUI()
        self.setupModels()
        self.applyLightTheme()
        
        self.resize(1024, 768)
        self.setWindowTitle("Система складского учета автозапчастей")

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
        self.themeToggleBtn.clicked.connect(self.toggleTheme)

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

        buttonLayout.addWidget(self.addBtn)
        buttonLayout.addWidget(self.editBtn)
        buttonLayout.addWidget(self.deleteBtn)
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
        catalogModel = QStandardItemModel(0, 4, self)
        catalogModel.setHorizontalHeaderLabels(["OEM-номер", "Наименование", "Марка/Модель", "Фото"])
        self.catalogTable.setModel(catalogModel)

        inventoryModel = QStandardItemModel(0, 6, self)
        inventoryModel.setHorizontalHeaderLabels(["Деталь", "OEM", "Марка/Модель", "Цена", "Количество", "Адрес склада"])
        self.inventoryTable.setModel(inventoryModel)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())