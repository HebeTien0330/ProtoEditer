'''
:@Author: tangchengqin
:@Date: 2025/1/8 17:16:40
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/13 20:22:16
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMainWindow
from PyQt5.QtCore import QDir, QModelIndex, Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from components.event import installEventSystem
from components.utils import getFileNameInPath
from components.cache import package, save, update, query, unpack

class CustomFileSystemModel(QFileSystemModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setNameFilters(["*.proto"])        # 只显示proto文件
        self.setNameFilterDisables(False)

    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        if flags & Qt.ItemIsEditable:
            flags &= ~Qt.ItemIsEditable
        return flags


class FileSystem:
    
    def __init__(self, window: QMainWindow):
        self.m_data = self.load()        # 文件系统数据
        self.m_window = window
        self.m_model = CustomFileSystemModel()
        self.m_model.setReadOnly(True)
        self.m_treeView = QTreeView()
        self.m_treeView.setModel(self.m_model)
        self.m_treeView.setRootIndex(self.m_model.index(QDir.rootPath()))
        self.m_treeView.setColumnWidth(0, 250)
        self.m_window.setCentralWidget(self.m_treeView)

        for col in range(1, self.m_model.columnCount()):      # 隐藏所有列，只显示文件名
            self.m_treeView.setColumnHidden(col, True)

        self.m_treeView.setAcceptDrops(True)
        self.m_treeView.setDragEnabled(True)
        self.m_treeView.setDropIndicatorShown(True)
        self.m_model.setReadOnly(False)

        self.m_treeView.dragEnterEvent = self.dragEnterEvent
        self.m_treeView.dropEvent = self.dropEvent

        installEventSystem(self)
        self.listen("onSave", self.save)
        self.listen("onOpenFile", self.onOpenFile)

        self.m_treeView.doubleClicked.connect(self.onFileDoubleClicked)
        self.afterInit()

    def save(self):
        update("fileSystem", package(self.m_data))
        save()
        print("save file system")

    def load(self):
        saveObj = query("fileSystem")
        if not saveObj:
            return {}
        return unpack(saveObj)

    def update(self, path):
        self.m_model.setRootPath(path)
        self.m_treeView.setRootIndex(self.m_model.index(path))
        self.m_data["path"] = path
        self.save()

    def afterInit(self):
        path = self.m_data.get("path")
        if not path:
            return
        self.update(path)

    def onOpenFile(self):
        folderPath = QFileDialog.getExistingDirectory(self.m_window, "打开文件夹", "")
        if not folderPath:
            return
        self.update(folderPath)

    def onFileDoubleClicked(self, index: QModelIndex):
        filePath = self.m_model.filePath(index)
        if QDir(filePath).exists():  # 确保是文件而不是文件夹
            return
        self.displayFile(filePath)

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
            viewMgr.swapView(getFileNameInPath(filePath))
