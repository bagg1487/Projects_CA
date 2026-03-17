#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>
#include <QTableView>
#include <QLineEdit>
#include <QPushButton>
#include <QComboBox>
#include <QCheckBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QStandardItemModel>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void toggleTheme();

private:
    bool isDarkMode;

    QTabWidget *tabWidget;
    QTableView *catalogTable;
    QTableView *inventoryTable;

    QLineEdit *searchEdit;
    QComboBox *brandFilter;
    QComboBox *conditionFilter;
    QComboBox *locationFilter;
    QCheckBox *inStockCheckbox;
    QPushButton *themeToggleBtn;

    QPushButton *addBtn;
    QPushButton *editBtn;
    QPushButton *deleteBtn;

    void setupUI();
    void setupModels();
    void applyLightTheme();
    void applyDarkTheme();
};

#endif
