'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:18:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 16:30:25
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QTabBar, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from components.utils import getFileNameInPath
from .viewPage import ViewPage
from .graphPage import GraphPage

class CustomTabBar(QTabBar):
    closeRequested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.onTabCloseRequested)
        self.m_closeButtons = {}

    def onTabCloseRequested(self, index):
        self.closeRequested.emit(index)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            pass
        else:
            super().mousePressEvent(event)

    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)
        size.setWidth(size.width() + 20)
        return size


class ViewsManager:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_viewPage = None
        self.m_graphMap = {}
        self.m_pathMap = {}
        self.m_tabs = QTabWidget()
        customTabBar = CustomTabBar(self.m_tabs)
        self.m_tabs.setTabBar(customTabBar)
        customTabBar.closeRequested.connect(self.onTabClose)
        self.m_tabs.currentChanged.connect(self.onTabChanged)
        self.m_customTabBar = customTabBar


    def createView(self, path, content):
        graphPage = GraphPage(self.m_window)
        graphWidget = graphPage.m_tab
        fileName = getFileNameInPath(path)
        index = self.m_tabs.addTab(graphWidget, fileName)
        self.m_tabs.setCurrentIndex(index)

        if not self.m_viewPage:
            self.m_viewPage = ViewPage(self.m_window)
        self.m_viewPage.update(content)

        self.m_graphMap[fileName] = graphPage
        self.m_pathMap[fileName] = path
        self.m_window.replaceMainContent(self.m_tabs)

    def updateView(self, path):
        content = self.getCurrentTabContent(path)
        self.m_viewPage.update(content)

    def switchView(self, fileName):
        index = list(self.m_pathMap.keys()).index(fileName)
        self.m_tabs.setCurrentIndex(index)

    def onTabChanged(self, index):
        fileName = self.m_tabs.tabText(index)
        if fileName not in self.m_graphMap:
            return
        path = self.m_pathMap.get(fileName)
        self.updateView(path)

    def getCurrentTabContent(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def onTabClose(self, index):
        self.m_tabs.removeTab(index)
        if self.m_tabs.count() > 0:
            return
        self.m_viewPage.update("")
