'''
:@Author: tangchengqin
:@Date: 2025/1/8 17:16:40
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 10:13:42
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtCore import QDir, QModelIndex, Qt, QEvent, QObject
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QKeyEvent
from components.event import installEventSystem
from components.utils import getFileNameInPath
from components.cache import package, save, update, query, unpack
import os

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


class FileSystemEventFilter(QObject):


    def __init__(self, file_system, tree_view, parent=None):
        super().__init__(parent)
        self.file_system = file_system
        self.tree_view = tree_view

    def eventFilter(self, obj, event):
        if obj == self.tree_view and event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() == Qt.Key_Delete:
                selected_index = self.tree_view.currentIndex()
                if selected_index.isValid():
                    self.file_system.deleteFile(selected_index)
                return True
        return super().eventFilter(obj, event)


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
        self.event_filter = FileSystemEventFilter(self, self.m_treeView)
        self.m_treeView.installEventFilter(self.event_filter)
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
        update("rootPath", package(path))
        self.save()

    def afterInit(self):
        path = self.m_data.get("path")
        if not path:
            return
        self.update(path)

    def getPath(self):
        return self.m_data.get("path")

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

    def newFile(self, filePath):
        self.onEvent("onNewFile", None, filePath)
        self.displayFile(filePath)

    def deleteFile(self, index: QModelIndex):
        filePath = self.m_model.filePath(index)
        if not filePath:
            QMessageBox.warning(self.m_window, "Warning", "file not found")
            return
        os.remove(filePath)
        self.m_model.removeRow(index.row(), index.parent())
        self.onEvent("onDeleteFile", None, filePath)

    def eventFilter(self, obj, event):
        if obj == self.m_treeView and event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            if key_event.key() == Qt.Key_Delete:
                selected_index = self.m_treeView.currentIndex()
                if selected_index.isValid():
                    self.deleteFile(selected_index)
                return True
        return super().eventFilter(obj, event)
