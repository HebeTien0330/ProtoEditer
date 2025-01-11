'''
:@Author: tangchengqin
:@Date: 2025/1/8 17:16:40
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 12:28:11
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMainWindow, QTextEdit
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from components.event import installEventSystem

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
        folder_path = QFileDialog.getExistingDirectory(self.m_window, "打开文件夹", "")
        if not folder_path:
            return
        self.update(folder_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if not event.mimeData().hasUrls():
            return
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls:
            return
        file_path = urls[0].toLocalFile()
        if QDir(file_path).exists():
            self.update(file_path)
        else:
            self.displayFile(file_path)

    def displayFile(self, file_path):
        viewMgr = self.m_window.getViewsManager()
        if not viewMgr:
            return
        with open(file_path, 'r') as file:
            content = file.read()
            viewMgr.createView(file_path, content)
