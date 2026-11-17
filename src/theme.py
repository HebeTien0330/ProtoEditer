'''
:@Author: tangchengqin
:@Date: 2026/11/18 01:30:00
:@LastEditors: tangchengqin
:@LastEditTime: 2026/11/18 01:30:00
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

def getAppStyle():
    return """
QMainWindow, QDialog {
    background: #1b1d27;
    color: #e8eaf3;
}
QWidget {
    color: #e8eaf3;
    font-size: 13px;
}
QMenuBar {
    background: #14161e;
    color: #e8eaf3;
    border-bottom: 1px solid #2c3142;
    padding: 2px 6px;
}
QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
    border-radius: 6px;
}
QMenuBar::item:selected {
    background: #2c3350;
}
QMenu {
    background: #222636;
    color: #e8eaf3;
    border: 1px solid #343a50;
    padding: 6px;
}
QMenu::item {
    padding: 7px 28px 7px 14px;
    border-radius: 6px;
}
QMenu::item:selected {
    background: #3e4e86;
}
QMenu::item:disabled {
    color: #6d7488;
}
QTreeView {
    background: #161821;
    border: none;
    outline: none;
    padding: 6px 0;
    alternate-background-color: #161821;
}
QTreeView::item {
    padding: 5px 8px;
    border-radius: 4px;
}
QTreeView::item:hover {
    background: #242838;
}
QTreeView::item:selected {
    background: #3e4e86;
    color: #ffffff;
}
QHeaderView::section {
    background: #161821;
    color: #9aa3b8;
    border: none;
    padding: 6px;
}
QTabWidget::pane {
    border: none;
    background: #1b1d27;
}
QTabBar::tab {
    background: #262a38;
    color: #b7bdd0;
    padding: 8px 16px;
    margin: 6px 4px 0 0;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background: #4c63d2;
    color: #ffffff;
}
QTabBar::tab:hover:!selected {
    background: #32384c;
}
QTextEdit, QPlainTextEdit, QLineEdit, QComboBox {
    background: #12141c;
    color: #e8eaf3;
    border: 1px solid #343a50;
    border-radius: 8px;
    padding: 6px 8px;
    selection-background-color: #3e4e86;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background: #222636;
    color: #e8eaf3;
    selection-background-color: #3e4e86;
    border: 1px solid #343a50;
}
QPushButton {
    background: #2a3044;
    color: #e8eaf3;
    border: 1px solid #3c435c;
    border-radius: 8px;
    padding: 7px 14px;
}
QPushButton:hover {
    background: #36405c;
}
QPushButton:pressed {
    background: #2c3350;
}
QPushButton#primaryButton {
    background: #4c63d2;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#primaryButton:hover {
    background: #5c72e0;
}
QLabel#titleLabel {
    font-size: 28px;
    font-weight: 600;
    color: #f4f6ff;
}
QLabel#panelTitle {
    font-size: 13px;
    font-weight: 600;
    color: #c5cbe0;
}
QLabel#mutedLabel {
    color: #9aa3b8;
}
QSplitter::handle {
    background: #2a2e3c;
}
QStatusBar {
    background: #14161e;
    color: #9aa3b8;
    border-top: 1px solid #2c3142;
}
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background: #3a4158;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 4px;
}
QScrollBar::handle:horizontal {
    background: #3a4158;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::add-line, QScrollBar::sub-line {
    width: 0;
    height: 0;
}
QGraphicsView {
    background: #14161e;
    border: none;
}
QMessageBox {
    background: #1b1d27;
}
QListWidget, QTableWidget {
    background: #161821;
    border: none;
    outline: none;
    gridline-color: #2c3142;
    alternate-background-color: #1b1d27;
}
QListWidget::item, QTableWidget::item {
    padding: 4px 6px;
}
QListWidget::item:selected, QTableWidget::item:selected {
    background: #3e4e86;
    color: #ffffff;
}
QTableWidget QLineEdit, QTableWidget QComboBox {
    border-radius: 4px;
}
"""
