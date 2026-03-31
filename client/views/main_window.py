from utils.algorithms import mergesort # Теперь импорт локальный и стабильный

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QCheckBox, QPushButton,
    QTableView, QTabWidget, QAbstractItemView,
    QDialog, QMessageBox, QLabel, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont,
    QStandardItemModel, QStandardItem
)
from typing import List

from models import Part
from controllers.part_controller import PartController
from views.dialogs import PartDialog, open_url
from views.card_view import CardView
from utils.theme import ThemeManager


class ThemeToggle(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dark = False
        self._thumb_x = 4
        self.setFixedSize(140, 36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._anim = QPropertyAnimation(self, b"thumb_x", self)
        self._anim.setDuration(220)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.toggled.connect(self._on_toggle)

    def get_thumb_x(self):
        return self._thumb_x

    def set_thumb_x(self, val):
        self._thumb_x = val
        self.update()

    thumb_x = pyqtProperty(int, fget=get_thumb_x, fset=set_thumb_x)

    def _on_toggle(self, checked: bool):
        self._dark = checked
        self._anim.stop()
        self._anim.setStartValue(self._thumb_x)
        self._anim.setEndValue(100 if checked else 4)
        self._anim.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r = h // 2
        track_col = QColor('#1c7ed6') if self._dark else QColor('#dee2e6')
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(track_col))
        p.drawRoundedRect(0, 0, w, h, r, r)
        p.setPen(QPen(QColor('#ffffff' if self._dark else '#495057')))
        f = QFont()
        f.setPointSize(9)
        f.setBold(True)
        p.setFont(f)
        if self._dark:
            p.drawText(8, 0, 80, h, Qt.AlignmentFlag.AlignVCenter, '☀  Светлая')
        else:
            p.drawText(38, 0, 90, h, Qt.AlignmentFlag.AlignVCenter, '🌙  Тёмная')
        thumb_size = h - 8
        p.setBrush(QBrush(QColor('#ffffff') if self._dark else QColor('#339af0')))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(self._thumb_x, 4, thumb_size, thumb_size)
        p.end()

class MergeSortProxyModel(QSortFilterProxyModel):
    def sort(self, column: int, order: Qt.SortOrder):
        if column < 0: return
        source_model = self.sourceModel()
        if not source_model: return

        rows_data = []
        for i in range(source_model.rowCount()):
            row_items = [source_model.item(i, j).clone() for j in range(source_model.columnCount())]
            rows_data.append(row_items)

        def key_func(row):
            text = row[column].text().strip()
            if not text:
                return (2, "")

            try:
                val = float(text.replace(' ', '').replace('₽', '').replace(',', '.'))
                return (0, val)
            except ValueError:
                return (1, text.lower())

        is_reverse = (order == Qt.SortOrder.DescendingOrder)
        sorted_data = mergesort(rows_data, key_func, is_reverse)

        source_model.setRowCount(0)
        for row in sorted_data:
            source_model.appendRow(row)

class MainWindow(QMainWindow):

    CAT_COLS = ['OEM-номер', 'Наименование', 'Марка/Модель', 'Годы', 'Фото', 'Магазин', '_id']
    INV_COLS = ['Деталь', 'OEM', 'Марка/Модель', 'Цена', 'Количество',
                'Состояние', 'Магазин', 'Адрес', 'Ссылка']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = PartController()
        self.theme_manager = ThemeManager()
        self._dark = False
        self._current_parts: List[Part] = []

        self.setupUI()
        self.setupModels()
        self.connectSignals()
        self.loadFilters()
        self.refreshData()
        self.applyLightTheme()

        self.resize(1200, 800)
        self.setWindowTitle('Система складского учёта автозапчастей')

    def setupUI(self):
        central = QWidget(self)
        root = QVBoxLayout(central)
        root.setSpacing(12)
        root.setContentsMargins(18, 16, 18, 16)

        root.addLayout(self._buildFilterPanel())
        root.addLayout(self._buildButtonPanel())

        self.tabWidget = QTabWidget(self)
        self._buildCatalogTableTab()
        self._buildCardTab()
        self._buildInventoryTab()
        root.addWidget(self.tabWidget)

        self.setCentralWidget(central)

    def _buildFilterPanel(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(8)

        self.searchEdit = QLineEdit(self)
        self.searchEdit.setPlaceholderText('Поиск по OEM, названию, марке/модели…')
        self.searchEdit.setMinimumWidth(280)

        self.brandFilter = QComboBox(self)
        self.brandFilter.addItem('Все марки')
        self.brandFilter.setMinimumWidth(130)

        self.conditionFilter = QComboBox(self)
        self.conditionFilter.addItems(['Любое состояние', 'NEW', 'USED'])

        self.locationFilter = QComboBox(self)
        self.locationFilter.addItem('Все склады')
        self.locationFilter.setMinimumWidth(140)

        self.inStockCheckbox = QCheckBox('Только в наличии', self)
        self.themeToggle = ThemeToggle(self)

        layout.addWidget(self.searchEdit)
        layout.addWidget(self.brandFilter)
        layout.addWidget(self.conditionFilter)
        layout.addWidget(self.locationFilter)
        layout.addWidget(self.inStockCheckbox)
        layout.addStretch()
        layout.addWidget(self.themeToggle)
        return layout

    def _buildButtonPanel(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        self.addBtn    = QPushButton('➕  Добавить', self)
        self.editBtn   = QPushButton('✏️  Редактировать', self)
        self.deleteBtn = QPushButton('🗑  Удалить', self)
        self.deleteBtn.setObjectName('deleteBtn')
        self.refreshBtn = QPushButton('🔄  Обновить', self)
        for btn in (self.addBtn, self.editBtn, self.deleteBtn, self.refreshBtn):
            layout.addWidget(btn)
        layout.addStretch()
        return layout

    def _buildCatalogTableTab(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(4, 4, 4, 4)
        self.catalogTable = QTableView(self)
        self._configureTable(self.catalogTable)
        hint = QLabel('💡 Кликните ячейку «Фото» или «Магазин» чтобы открыть ссылку')
        hint.setStyleSheet('color: #868e96; font-size: 11px; padding: 2px 4px;')
        lay.addWidget(self.catalogTable)
        lay.addWidget(hint)
        self.tabWidget.addTab(tab, '📋  Таблица')

    def _buildCardTab(self):
        self.cardView = CardView(self)
        self.cardView.edit_requested.connect(self._editPartById)
        self.cardView.delete_requested.connect(self._deletePartById)
        self.tabWidget.addTab(self.cardView, '🗂  Карточки')

    def _buildInventoryTab(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(4, 4, 4, 4)
        self.inventoryTable = QTableView(self)
        self._configureTable(self.inventoryTable)
        hint = QLabel('💡 Кликните ячейку «Ссылка» чтобы открыть магазин')
        hint.setStyleSheet('color: #868e96; font-size: 11px; padding: 2px 4px;')
        lay.addWidget(self.inventoryTable)
        lay.addWidget(hint)
        self.tabWidget.addTab(tab, '🏭  Наличие по складам')

    @staticmethod
    def _configureTable(table: QTableView):
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionsClickable(True)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setDefaultSectionSize(28)
        table.verticalHeader().hide()

    def setupModels(self):
        self.catalogModel = QStandardItemModel(0, len(self.CAT_COLS), self)
        self.catalogModel.setHorizontalHeaderLabels(self.CAT_COLS)

        self.catalogProxy = MergeSortProxyModel(self)
        self.catalogProxy.setSourceModel(self.catalogModel)

        self.catalogTable.setModel(self.catalogProxy)
        self.catalogTable.setSortingEnabled(True)
        self.catalogTable.setColumnHidden(len(self.CAT_COLS) - 1, True)

        self.inventoryModel = QStandardItemModel(0, len(self.INV_COLS), self)
        self.inventoryModel.setHorizontalHeaderLabels(self.INV_COLS)

        self.inventoryProxy = MergeSortProxyModel(self)
        self.inventoryProxy.setSourceModel(self.inventoryModel)

        self.inventoryTable.setModel(self.inventoryProxy)
        self.inventoryTable.setSortingEnabled(True)

    def connectSignals(self):
        self.searchEdit.textChanged.connect(self.refreshData)
        self.brandFilter.currentTextChanged.connect(self.refreshData)
        self.conditionFilter.currentTextChanged.connect(self.refreshData)
        self.locationFilter.currentTextChanged.connect(self.refreshData)
        self.inStockCheckbox.stateChanged.connect(self.refreshData)
        self.themeToggle.toggled.connect(self._onThemeToggled)
        self.addBtn.clicked.connect(self.addPart)
        self.editBtn.clicked.connect(self.editPart)
        self.deleteBtn.clicked.connect(self.deletePart)
        self.refreshBtn.clicked.connect(self.refreshData)
        self.catalogTable.clicked.connect(self._onCatalogCellClick)
        self.inventoryTable.clicked.connect(self._onInventoryCellClick)

    def loadFilters(self):
        try:
            for brand in self.controller.get_brands():
                self.brandFilter.addItem(brand)
            for loc in self.controller.get_locations():
                self.locationFilter.addItem(loc)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить фильтры:\n{e}')

    def refreshData(self):
        self._loadCatalog()
        self._loadInventory()

    def _loadCatalog(self):
        try:
            parts = self.controller.get_all_parts(
                search=self.searchEdit.text(),
                brand=self.brandFilter.currentText(),
                condition=self.conditionFilter.currentText(),
                location=self.locationFilter.currentText(),
                in_stock_only=self.inStockCheckbox.isChecked()
            )
            self._current_parts = parts

            self.catalogModel.setRowCount(0)
            for p in parts:
                row_items = [
                    QStandardItem(p.oem_number or ''),
                    QStandardItem(p.part_name or ''),
                    QStandardItem(p.car_info),
                    QStandardItem(p.years_display),
                    self._link_item(p.photo_url, '🖼 Фото'),
                    self._link_item(p.shop_url, '🔗 Магазин'),
                    QStandardItem(str(p.id)),
                ]
                self.catalogModel.appendRow(row_items)

            for i in range(len(self.CAT_COLS) - 1):
                self.catalogTable.resizeColumnToContents(i)

            self.cardView.set_parts(parts)

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить каталог:\n{e}')

    def _loadInventory(self):
        try:
            items = self.controller.get_inventory()
            self.inventoryModel.setRowCount(0)
            for it in items:
                row_items = [
                    QStandardItem(it.part_name),
                    QStandardItem(it.oem_number),
                    QStandardItem(it.car_model),
                    QStandardItem(str(it.price)),
                    QStandardItem(str(it.quantity)),
                    QStandardItem(it.condition.upper()),
                    QStandardItem(it.store_name),
                    QStandardItem(it.address),
                    self._link_item(it.shop_url, '🔗 Открыть'),
                ]
                self.inventoryModel.appendRow(row_items)
            for i in range(len(self.INV_COLS)):
                self.inventoryTable.resizeColumnToContents(i)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить инвентарь:\n{e}')

    @staticmethod
    def _link_item(url: str | None, label: str) -> QStandardItem:
        if url and url.strip():
            item = QStandardItem(label)
            item.setData(url.strip(), Qt.ItemDataRole.UserRole)
            item.setForeground(QColor('#1c7ed6'))
            item.setToolTip(url.strip())
        else:
            item = QStandardItem('—')
            item.setForeground(QColor('#868e96'))
        return item

    def _onCatalogCellClick(self, proxy_index):
        if proxy_index.column() in (4, 5):
            src = self.catalogProxy.mapToSource(proxy_index)
            url = self.catalogModel.itemFromIndex(src).data(Qt.ItemDataRole.UserRole)
            if url:
                open_url(url)

    def _onInventoryCellClick(self, proxy_index):
        if proxy_index.column() == 8:
            src = self.inventoryProxy.mapToSource(proxy_index)
            url = self.inventoryModel.itemFromIndex(src).data(Qt.ItemDataRole.UserRole)
            if url:
                open_url(url)

    def addPart(self):
        dialog = PartDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.controller.add_part(dialog.getData())
                self.refreshData()
                QMessageBox.information(self, 'Готово', 'Запчасть добавлена.')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def editPart(self):
        part_id = self._selectedPartId()
        if part_id is None:
            QMessageBox.warning(self, 'Внимание', 'Выберите запчасть в таблице для редактирования.')
            return
        self._editPartById(part_id)

    def _editPartById(self, part_id: int):
        part = self.controller.get_part(part_id)
        if not part:
            QMessageBox.warning(self, 'Ошибка', 'Запчасть не найдена.')
            return
        dialog = PartDialog(self, part)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                self.controller.update_part(part_id, dialog.getData())
                self.refreshData()
                QMessageBox.information(self, 'Готово', 'Запчасть обновлена.')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def deletePart(self):
        part_id = self._selectedPartId()
        if part_id is None:
            QMessageBox.warning(self, 'Внимание', 'Выберите запчасть в таблице для удаления.')
            return
        self._deletePartById(part_id)

    def _deletePartById(self, part_id: int):
        part = self.controller.get_part(part_id)
        name = part.part_name if part else f'ID={part_id}'
        reply = QMessageBox.question(
            self, 'Подтверждение', f"Удалить «{name}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.controller.delete_part(part_id):
                    self.refreshData()
                    QMessageBox.information(self, 'Готово', 'Запчасть удалена.')
                else:
                    QMessageBox.warning(self, 'Ошибка', 'Запчасть не найдена.')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))

    def _selectedPartId(self) -> int | None:
        selected = self.catalogTable.selectedIndexes()
        if not selected:
            return None
        id_proxy = self.catalogProxy.index(selected[0].row(), len(self.CAT_COLS) - 1)
        id_src   = self.catalogProxy.mapToSource(id_proxy)
        item     = self.catalogModel.itemFromIndex(id_src)
        if item and item.text():
            return int(item.text())
        return None

    def _onThemeToggled(self, dark: bool):
        self._dark = dark
        if dark:
            self.applyDarkTheme()
        else:
            self.applyLightTheme()
        self.cardView.set_dark(dark)

    def applyLightTheme(self):
        self.setStyleSheet(self.theme_manager.light_theme())

    def applyDarkTheme(self):
        self.setStyleSheet(self.theme_manager.dark_theme())
