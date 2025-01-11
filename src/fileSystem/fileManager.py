'''
:@Author: tangchengqin
:@Date: 2025/1/8 17:16:40
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 16:21:25
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMainWindow, QTextEdit
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from components.event import installEventSystem
from components.utils import getFileNameInPath

class FileSystem:
    
    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_model = QFileSystemModel()
        self.m_treeView = QTreeView()
        self.m_treeView.setModel(self.m_model)
        self.m_treeView.setRootIndex(self.m_model.index(QDir.rootPath()))
        self.m_treeView.setColumnWidth(0, 250)
        self.m_window.setCentralWidget(self.m_treeView)

        self.m_treeView.setAcceptDrops(True)
        self.m_treeView.setDragEnabled(True)
        self.m_treeView.setDropIndicatorShown(True)
        self.m_model.setReadOnly(False)

        self.m_treeView.dragEnterEvent = self.dragEnterEvent
        self.m_treeView.dropEvent = self.dropEvent

        installEventSystem(self)
        self.listen("onOpenFile", self.onOpenFile)

    def update(self, path):
        self.m_model.setRootPath(path)
        self.m_treeView.setRootIndex(self.m_model.index(path))

    def onOpenFile(self):
        folderPath = QFileDialog.getExistingDirectory(self.m_window, "打开文件夹", "")
        if not folderPath:
            return
        self.update(folderPath)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if not event.mimeData().hasUrls():
            return
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls:
            return
        filePath = urls[0].toLocalFile()
        if QDir(filePath).exists():
            self.update(filePath)
        else:
            self.displayFile(filePath)

    def displayFile(self, filePath):
        viewMgr = self.m_window.getViewsManager()
        if not viewMgr:
            return
        with open(filePath, 'r') as file:
            content = file.read()
            viewMgr.createView(filePath, content)
            viewMgr.switchView(getFileNameInPath(filePath))
