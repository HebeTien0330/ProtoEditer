'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:18:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 16:26:36
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget
from components.utils import getFileNameInPath
from .viewPage import ViewPage
from .graphPage import GraphPage

class ViewsManager:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_viewPage = None
        self.m_graphMap = {}
        self.m_pathMap = {}
        self.m_tabs = QTabWidget()
        self.m_tabs.currentChanged.connect(self.onTabChanged)

    def createView(self, path, content):
        graphPage = GraphPage(self.m_window)
        graphWidget = graphPage.m_tab
        fileName = getFileNameInPath(path)
        self.m_tabs.addTab(graphWidget, fileName)

        if not self.m_viewPage:
            self.m_viewPage = ViewPage(self.m_window)
        self.m_viewPage.update(content)

        self.m_graphMap[fileName] = graphPage
        self.m_pathMap[fileName] = path
        self.m_window.replaceMainContent(self.m_tabs)

    def updateView(self, path, content):
        pass

    def switchView(self, fileName):
        index = list(self.m_pathMap.keys()).index(fileName)
        self.m_tabs.setCurrentIndex(index)

    def onTabChanged(self, index):
        fileName = self.m_tabs.tabText(index)
        if fileName not in self.m_graphMap:
            return
        path = self.m_pathMap.get(fileName)
        content = self.getCurrentTabContent(path)
        self.m_viewPage.update(content)

    def getCurrentTabContent(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading {path}: {str(e)}"
