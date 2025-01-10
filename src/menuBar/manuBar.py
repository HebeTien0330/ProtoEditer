'''
:@Author: tangchengqin
:@Date: 2025/1/8 16:39:24
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/8 16:39:24
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QAction

class ManuBarManager:

    def __init__(self, window):
        self.m_window = window
        self.m_menuMap = {}

    def getMenuBar(self):
        """
        获取菜单栏
        :return: 菜单栏
        """
        return self.m_window.menuBar()

    def addMenu(self, menuName, menuAction, callback=None):
        """
        添加菜单
        :param menuName: 菜单名称
        :param menuAction: 菜单动作
        :param callback: 回调函数
        :return: None
        """
        menu = self.m_menuMap.get(menuName)
        if menu is None:
            menu = self.getMenuBar().addMenu(menuName)
            self.m_menuMap[menuName] = menu
        action = QAction(menuAction, self.m_window)
        if callback is not None:
            action.triggered.connect(callback)
        menu.addAction(action)


