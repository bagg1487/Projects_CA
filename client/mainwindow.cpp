#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), isDarkMode(false) {
    setupUI();
    setupModels();
    applyLightTheme();

    resize(1024, 768);
    setWindowTitle("Система складского учета автозапчастей");
}

MainWindow::~MainWindow() {}

void MainWindow::setupUI() {
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->setSpacing(15);
    mainLayout->setContentsMargins(20, 20, 20, 20);

    QHBoxLayout *topPanelLayout = new QHBoxLayout();
    topPanelLayout->setSpacing(10);

    searchEdit = new QLineEdit(this);
    searchEdit->setPlaceholderText("Поиск по OEM, названию или марке/модели...");
    searchEdit->setMinimumWidth(300);

    brandFilter = new QComboBox(this);
    brandFilter->addItem("Все марки");

    conditionFilter = new QComboBox(this);
    conditionFilter->addItem("Любое состояние");
    conditionFilter->addItem("NEW");
    conditionFilter->addItem("USED");

    locationFilter = new QComboBox(this);
    locationFilter->addItem("Все склады");

    inStockCheckbox = new QCheckBox("Только в наличии", this);

    themeToggleBtn = new QPushButton("🌙 Тёмная тема", this);
    themeToggleBtn->setCursor(Qt::PointingHandCursor);
    connect(themeToggleBtn, &QPushButton::clicked, this, &MainWindow::toggleTheme);

    topPanelLayout->addWidget(searchEdit);
    topPanelLayout->addWidget(brandFilter);
    topPanelLayout->addWidget(conditionFilter);
    topPanelLayout->addWidget(locationFilter);
    topPanelLayout->addWidget(inStockCheckbox);
    topPanelLayout->addStretch();
    topPanelLayout->addWidget(themeToggleBtn);

    QHBoxLayout *buttonLayout = new QHBoxLayout();
    addBtn = new QPushButton("Добавить деталь", this);
    editBtn = new QPushButton("Редактировать", this);
    deleteBtn = new QPushButton("Удалить", this);
    deleteBtn->setObjectName("deleteBtn");

    buttonLayout->addWidget(addBtn);
    buttonLayout->addWidget(editBtn);
    buttonLayout->addWidget(deleteBtn);
    buttonLayout->addStretch();

    tabWidget = new QTabWidget(this);

    QWidget *catalogTab = new QWidget();
    QVBoxLayout *catalogLayout = new QVBoxLayout(catalogTab);
    catalogTable = new QTableView(this);
    catalogTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    catalogTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    catalogTable->horizontalHeader()->setStretchLastSection(true);
    catalogLayout->addWidget(catalogTable);

    QWidget *inventoryTab = new QWidget();
    QVBoxLayout *inventoryLayout = new QVBoxLayout(inventoryTab);
    inventoryTable = new QTableView(this);
    inventoryTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    inventoryTable->setEditTriggers(QAbstractItemView::NoEditTriggers);
    inventoryTable->horizontalHeader()->setStretchLastSection(true);
    inventoryLayout->addWidget(inventoryTable);

    tabWidget->addTab(catalogTab, "Каталог запчастей");
    tabWidget->addTab(inventoryTab, "Наличие по складам");

    mainLayout->addLayout(topPanelLayout);
    mainLayout->addLayout(buttonLayout);
    mainLayout->addWidget(tabWidget);

    setCentralWidget(centralWidget);
}

void MainWindow::setupModels() {
    QStandardItemModel *catalogModel = new QStandardItemModel(0, 4, this);
    catalogModel->setHorizontalHeaderLabels({"OEM-номер", "Наименование", "Марка/Модель", "Фото"});
    catalogTable->setModel(catalogModel);

    QStandardItemModel *inventoryModel = new QStandardItemModel(0, 6, this);
    inventoryModel->setHorizontalHeaderLabels({"Деталь", "OEM", "Марка/Модель", "Цена", "Количество", "Адрес склада"});
    inventoryTable->setModel(inventoryModel);
}

void MainWindow::toggleTheme() {
    isDarkMode = !isDarkMode;
    if (isDarkMode) {
        themeToggleBtn->setText("☀️ Светлая тема");
        applyDarkTheme();
    } else {
        themeToggleBtn->setText("🌙 Тёмная тема");
        applyLightTheme();
    }
}

void MainWindow::applyLightTheme() {
    QString styleSheet = R"(
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
    )";
    this->setStyleSheet(styleSheet);
}

void MainWindow::applyDarkTheme() {
    QString styleSheet = R"(
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
    )";
    this->setStyleSheet(styleSheet);
}
