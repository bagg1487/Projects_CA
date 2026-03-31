class ThemeManager:

    @staticmethod
    def light_theme() -> str:
        return """
        QMainWindow, QDialog {
            background-color: #f4f6f9;
            color: #212529;
        }
        QWidget {
            background-color: #f4f6f9;
            color: #212529;
            font-size: 13px;
        }
        QScrollArea {
            background-color: #f4f6f9;
            border: none;
        }
        QScrollArea > QWidget > QWidget {
            background-color: #f4f6f9;
        }
        QTabWidget::pane {
            border: 1px solid #dee2e6;
            border-radius: 6px;
            background-color: #ffffff;
        }
        QTabWidget::pane > QWidget {
            background-color: #ffffff;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 7px 11px;
            border: 1px solid #ced4da;
            border-radius: 6px;
            background-color: #ffffff;
            color: #212529;
            font-size: 13px;
            min-height: 22px;
        }
        QLineEdit:focus, QComboBox:focus,
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #4dabf7;
            background-color: #ffffff;
        }
        QLineEdit:disabled, QComboBox:disabled {
            background-color: #e9ecef;
            color: #868e96;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #212529;
            border: 1px solid #ced4da;
            selection-background-color: #e7f5ff;
            selection-color: #212529;
            outline: none;
        }
        QComboBox::drop-down { border: none; }
        QComboBox::down-arrow { image: none; width: 0px; }
        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {
            background-color: #e9ecef;
            border: none;
            width: 20px;
        }
        QPushButton {
            padding: 8px 18px;
            background-color: #339af0;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover  { background-color: #228be6; }
        QPushButton:pressed { background-color: #1c7ed6; }
        QPushButton#deleteBtn { background-color: #fa5252; }
        QPushButton#deleteBtn:hover  { background-color: #f03e3e; }
        QPushButton#deleteBtn:pressed { background-color: #e03131; }
        QTableView {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            gridline-color: #f1f3f5;
            selection-background-color: #d0ebff;
            selection-color: #1864ab;
            alternate-background-color: #f8f9fa;
        }
        QTableView::item { padding: 4px 8px; color: #212529; background-color: transparent; }
        QTableView::item:selected {
            background-color: #d0ebff;
            color: #1864ab;
        }
        QHeaderView { background-color: #f8f9fa; }
        QHeaderView::section {
            background-color: #f8f9fa;
            padding: 8px 10px;
            border: none;
            border-bottom: 2px solid #dee2e6;
            font-weight: 700;
            color: #495057;
        }
        QHeaderView::section:hover { background-color: #e9ecef; }
        QTabBar::tab {
            background: #e9ecef;
            padding: 9px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            color: #495057;
        }
        QTabBar::tab:selected {
            background: #ffffff;
            border: 1px solid #dee2e6;
            border-bottom-color: #ffffff;
            font-weight: 700;
            color: #212529;
        }
        QTabBar::tab:hover:!selected { background: #dee2e6; }
        QCheckBox { spacing: 6px; background-color: transparent; }
        QCheckBox::indicator {
            width: 16px; height: 16px;
            border: 1px solid #adb5bd;
            border-radius: 3px;
            background: #ffffff;
        }
        QCheckBox::indicator:checked {
            background-color: #339af0;
            border-color: #339af0;
        }
        QScrollBar:vertical {
            background: #f1f3f5; width: 8px; border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #ced4da; border-radius: 4px; min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QLabel { color: #212529; background: transparent; }
        QDialogButtonBox QPushButton { min-width: 90px; }
        QMessageBox { background-color: #ffffff; }
        QMessageBox QLabel { color: #212529; }
        """

    @staticmethod
    def dark_theme() -> str:
        return """
        QMainWindow, QDialog {
            background-color: #1a1b1e;
            color: #c1c2c5;
        }
        QWidget {
            background-color: #1a1b1e;
            color: #c1c2c5;
            font-size: 13px;
        }
        QScrollArea {
            background-color: #1a1b1e;
            border: none;
        }
        QScrollArea > QWidget > QWidget {
            background-color: #1a1b1e;
        }
        QTabWidget::pane {
            border: 1px solid #373a40;
            border-radius: 6px;
            background-color: #1e1f23;
        }
        QTabWidget::pane > QWidget {
            background-color: #1e1f23;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 7px 11px;
            border: 1px solid #373a40;
            border-radius: 6px;
            background-color: #25262b;
            color: #c1c2c5;
            font-size: 13px;
            min-height: 22px;
        }
        QLineEdit:focus, QComboBox:focus,
        QSpinBox:focus, QDoubleSpinBox:focus {
            border: 1px solid #339af0;
            background-color: #2c2d33;
        }
        QLineEdit:disabled, QComboBox:disabled {
            background-color: #1e1f23;
            color: #5c5f66;
        }
        QComboBox QAbstractItemView {
            background-color: #25262b;
            color: #c1c2c5;
            border: 1px solid #373a40;
            selection-background-color: #1864ab;
            selection-color: #ffffff;
            outline: none;
        }
        QComboBox::drop-down { border: none; }
        QComboBox::down-arrow { image: none; width: 0px; }
        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {
            background-color: #373a40;
            border: none;
            width: 20px;
            color: #c1c2c5;
        }
        QPushButton {
            padding: 8px 18px;
            background-color: #1c7ed6;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
        }
        QPushButton:hover  { background-color: #1971c2; }
        QPushButton:pressed { background-color: #1864ab; }
        QPushButton#deleteBtn { background-color: #c92a2a; }
        QPushButton#deleteBtn:hover  { background-color: #b02020; }
        QPushButton#deleteBtn:pressed { background-color: #962020; }
        QTableView {
            background-color: #25262b;
            border: 1px solid #373a40;
            border-radius: 6px;
            gridline-color: #2c2e33;
            selection-background-color: #1864ab;
            selection-color: #ffffff;
            alternate-background-color: #2a2b30;
            color: #c1c2c5;
        }
        QTableView::item { padding: 4px 8px; color: #c1c2c5; background-color: transparent; }
        QTableView::item:selected {
            background-color: #1864ab;
            color: #ffffff;
        }
        QTableView::item:alternate { background-color: #2a2b30; }
        QHeaderView { background-color: #1e1f23; }
        QHeaderView::section {
            background-color: #1e1f23;
            color: #909296;
            padding: 8px 10px;
            border: none;
            border-bottom: 2px solid #373a40;
            font-weight: 700;
        }
        QHeaderView::section:hover { background-color: #25262b; }
        QTableView QTableCornerButton::section {
            background-color: #1e1f23;
            border: none;
            border-bottom: 2px solid #373a40;
        }
        QTabBar::tab {
            background: #25262b;
            padding: 9px 20px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            color: #909296;
        }
        QTabBar::tab:selected {
            background: #1e1f23;
            border: 1px solid #373a40;
            border-bottom-color: #1e1f23;
            font-weight: 700;
            color: #c1c2c5;
        }
        QTabBar::tab:hover:!selected { background: #2c2e33; }
        QCheckBox { spacing: 6px; color: #c1c2c5; background-color: transparent; }
        QCheckBox::indicator {
            width: 16px; height: 16px;
            border: 1px solid #5c5f66;
            border-radius: 3px;
            background: #25262b;
        }
        QCheckBox::indicator:checked {
            background-color: #1c7ed6;
            border-color: #1c7ed6;
        }
        QScrollBar:vertical {
            background: #1e1f23; width: 8px; border-radius: 4px;
        }
        QScrollBar::handle:vertical {
            background: #5c5f66; border-radius: 4px; min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QScrollBar:horizontal {
            background: #1e1f23; height: 8px; border-radius: 4px;
        }
        QScrollBar::handle:horizontal {
            background: #5c5f66; border-radius: 4px; min-width: 30px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
        QLabel { color: #c1c2c5; background: transparent; }
        QDialogButtonBox QPushButton { min-width: 90px; }
        QMessageBox { background-color: #25262b; }
        QMessageBox QLabel { color: #c1c2c5; }
        QFormLayout QLabel { color: #909296; }
        QToolTip {
            background-color: #25262b;
            color: #c1c2c5;
            border: 1px solid #373a40;
            padding: 4px 8px;
            border-radius: 4px;
        }
        """
