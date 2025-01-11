'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:18:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 15:54:02
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QTabWidget
from components.utils import getFileNameInPath
from .viewPage import ViewPage
from .graphPage import GraphPage

class ViewsManager:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_viewsMap = {}
        self.m_tabs = QTabWidget()

    def createView(self, path, content):
        graphPage = GraphPage(self.m_window)
        graphWidget = graphPage.m_tab
        self.m_tabs.addTab(graphWidget, getFileNameInPath(path))

        viewPage = ViewPage(self.m_window)
        viewPage.update(content)

        self.m_viewsMap[path] = [graphPage, viewPage]

        self.m_window.replaceMainContent(self.m_tabs)

    def updateView(self, path, content):
        pass
