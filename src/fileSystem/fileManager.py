'''
:@Author: tangchengqin
:@Date: 2025/1/8 17:16:40
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/8 17:16:40
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QFileDialog
from PyQt5.QtCore import QDir
from components.event import installEventSystem

class FileSystem:
    
    def __init__(self, window):
        self.m_window = window
        self.m_model = QFileSystemModel()
        self.m_treeView = QTreeView()
        self.m_treeView.setModel(self.m_model)
        self.m_treeView.setRootIndex(self.m_model.index(QDir.rootPath()))
        self.m_treeView.setColumnWidth(0, 250)
        self.m_window.setCentralWidget(self.m_treeView)

        installEventSystem(self)
        self.listen("onOpenFile", self.onOpenFile)

    def update(self, path):
        self.m_model.setRootPath(path)
        self.m_treeView.setRootIndex(self.m_model.index(path))

    def onOpenFile(self):
        folder_path = QFileDialog.getExistingDirectory(self.m_window, "打开文件夹", "")
        if folder_path:
            self.update(folder_path)
