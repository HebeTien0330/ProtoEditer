'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:18:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 12:18:58
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow
from .viewPage import ViewPage

class ViewsManager:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_viewsMap = {}

    def createView(self, path, content):
        viewPage = ViewPage(self.m_window)
        viewPage.update(content)
        self.m_viewsMap[path] = viewPage

    def updateView(self, path, content):
        pass
