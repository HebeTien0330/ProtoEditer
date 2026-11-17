'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:18:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/18 11:29:46
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QTabBar, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from components.utils import getFileNameInPath
from components.cache import package, save, update, query, unpack
from components.event import installEventSystem
from .viewPage import ViewPage
from .protoEditorPage import ProtoEditorPage
import os

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
        self.m_pageMap = {}
        self.m_pathMap = {}
        self.m_tabs = QTabWidget()
        customTabBar = CustomTabBar(self.m_tabs)
        self.m_tabs.setTabBar(customTabBar)
        customTabBar.closeRequested.connect(self.onTabClose)
        self.m_tabs.currentChanged.connect(self.onTabChanged)
        self.m_customTabBar = customTabBar
        installEventSystem(self)
        self.listen("onSave", self.save)
        self.listen("onRefreshViews", self.refreshCurrentView)
        self.listen("onDeleteFile", self.deleteFile)
        self.listen("onNewProject", self.onNewProject)
        self.load()

    def save(self):
        for page in self.m_pageMap.values():
            page.saveFile()
        tabsInfo = []
        for fileName, path in self.m_pathMap.items():
            content = self.getCurrentTabContent(path)
            tabsInfo.append({'fileName': fileName, 'path': path, 'content': content})
        update("tabsInfo", package(tabsInfo))
        save()
        print("save file system")

    def load(self):
        saveObj = query("tabsInfo")
        if not saveObj:
            return
        tabsInfo = unpack(saveObj)
        for tab in tabsInfo:
            self.createView(tab['path'], tab['content'])

    def getIndexByFileName(self, fileName):
        fileNames = list(self.m_pathMap.keys())
        if fileName not in fileNames:
            return -1
        return fileNames.index(fileName)

    def createView(self, path, content):
        if not os.path.exists(path):
            print("file not exists")
            return 
        fileName = getFileNameInPath(path)
        # 检查文件是否已经打开
        if fileName in self.m_pageMap:
            self.swapView(fileName)
            return
        if not self.m_viewPage:
            self.m_viewPage = ViewPage(self.m_window)
        page = ProtoEditorPage(self.m_window)
        page.bindPreview(self.m_viewPage)
        page.load(path, content)
        index = self.m_tabs.addTab(page.m_tab, fileName)
        self.m_tabs.setCurrentIndex(index)
        self.m_pageMap[fileName] = page
        self.m_pathMap[fileName] = path
        self.m_window.replaceMainContent(self.m_tabs)

    def updateView(self, fileName, mode="all"):
        page = self.m_pageMap.get(fileName)
        path = self.m_pathMap.get(fileName)
        if not page or not path:
            return
        if page.m_dirty:
            if self.m_viewPage:
                self.m_viewPage.update(page.m_text)
                page.revealCurrent()
            return
        content = self.getCurrentTabContent(path)
        page.bindPreview(self.m_viewPage)
        page.load(path, content)

    def swapView(self, fileName):
        index = self.getIndexByFileName(fileName)
        if index < 0:
            return
        self.m_tabs.setCurrentIndex(index)

    def onTabChanged(self, index):
        fileName = self.m_tabs.tabText(index)
        if fileName not in self.m_pageMap:
            return
        self.updateView(fileName)

    def getCurrentTabContent(self, path):
        if not os.path.exists(path):
            return ""
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def onTabClose(self, index):
        fileName = self.m_tabs.tabText(index)
        page = self.m_pageMap.get(fileName)
        if page and page.m_dirty:
            reply = QMessageBox.question(
                self.m_window,
                "保存",
                "保存对 %s 的修改吗？" % fileName,
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes,
            )
            if reply == QMessageBox.Cancel:
                return
            if reply == QMessageBox.Yes:
                page.saveFile()
        self.m_tabs.removeTab(index)
        del self.m_pathMap[fileName]
        del self.m_pageMap[fileName]
        if self.m_tabs.count() > 0:
            return
        if self.m_viewPage:
            self.m_viewPage.update("")
        self.m_window.showWelcome()
        self.save()

    def onNewProject(self):
        while self.m_tabs.count():
            self.m_tabs.removeTab(0)
        self.m_pathMap.clear()
        self.m_pageMap.clear()
        if self.m_viewPage:
            self.m_viewPage.update("")
        self.m_window.showWelcome()
        self.save()

    def refreshCurrentView(self, mode="all"):
        currentIndex = self.m_tabs.currentIndex()
        if currentIndex < 0:
            return  # 没有选中的标签页
        fileName = self.m_tabs.tabText(currentIndex)
        path = self.m_pathMap.get(fileName)
        if not path:
            return  # 路径不存在
        self.updateView(fileName, mode)

    def focusSearch(self):
        index = self.m_tabs.currentIndex()
        if index < 0:
            return
        fileName = self.m_tabs.tabText(index)
        page = self.m_pageMap.get(fileName)
        if not page:
            return
        page.focusSearch()

    def deleteFile(self, filePath):
        fileName = getFileNameInPath(filePath)
        index = self.getIndexByFileName(fileName)
        if index < 0:
            return
        self.onTabClose(index)
