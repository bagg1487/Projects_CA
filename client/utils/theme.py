class ThemeManager:
    """Управление темами оформления"""

    @staticmethod
    def light_theme() -> str:
        return """
        QMainWindow { background-color: #f4f6f9; color: #212529; }
        QWidget { color: #212529; }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
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

    @staticmethod
    def dark_theme() -> str:
        return """
        QMainWindow { background-color: #121212; color: #e0e0e0; }
        QWidget { color: #e0e0e0; }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
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