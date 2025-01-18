'''
:@Author: tangchengqin
:@Date: 2025/1/18 11:44:35
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/18 14:03:32
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QSpacerItem, QSizePolicy
import os

class ExportManager:

    def __init__(self, window):
        self.m_window = window
        defaultPath = os.getcwd()
        self.m_exportFolder = defaultPath
        self.m_exportPath = defaultPath
        self.m_exportScript = defaultPath

    def createExportDialog(self):
        dialog = QDialog(self.m_window)
        dialog.setWindowTitle("Export Options")
        dialog.resize(500, 200)
        layout = QVBoxLayout()
        # 按钮和路径显示框：选择目标导出文件夹
        folderLayout = self.createExportFolder(dialog)
        layout.addLayout(folderLayout)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # 按钮和路径显示框：选择导出路径
        pathLayout = self.createExportPath(dialog)
        layout.addLayout(pathLayout)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # 按钮和路径显示框：选择导出脚本
        scriptLayout = self.createExportScript(dialog)
        layout.addLayout(scriptLayout)
        self.populateScriptComboBox()
        layout.addItem(QSpacerItem(30, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        # 添加导出和取消按钮
        btnLayout = QHBoxLayout()
        btnExport = QPushButton("Export", dialog)
        btnExport.clicked.connect(lambda: self.doExport(self.m_exportPath))
        btnCancel = QPushButton("Cancel", dialog)
        btnCancel.clicked.connect(dialog.reject)
        btnLayout.addWidget(btnExport)
        btnLayout.addWidget(btnCancel)
        layout.addLayout(btnLayout)
        dialog.setLayout(layout)
        dialog.exec_()

    def createExportFolder(self, dialog):
        # 按钮和路径显示框：选择目标导出文件夹
        folderLayout = QVBoxLayout()
        folderLabel = QLabel("Select Export Folder:", dialog)
        folderLayout.addWidget(folderLabel)
        folderEditLayout = QHBoxLayout()
        self.m_folderEdit = QLineEdit(self.m_exportFolder, dialog)
        self.m_folderEdit.setFixedWidth(300)
        folderEditLayout.addWidget(self.m_folderEdit)
        btnFolder = QPushButton("Path", dialog)
        btnFolder.setFixedWidth(150)
        btnFolder.clicked.connect(self.chooseExportFolder)
        folderEditLayout.addWidget(btnFolder)
        folderLayout.addLayout(folderEditLayout)
        return folderLayout

    def createExportPath(self, dialog):
        pathLayout = QVBoxLayout()
        pathLabel = QLabel("Select Export Path:", dialog)
        pathLayout.addWidget(pathLabel)
        pathEditLayout = QHBoxLayout()
        self.m_pathEdit = QLineEdit(self.m_exportPath, dialog)
        self.m_pathEdit.setFixedWidth(300)  # 设置固定宽度
        pathEditLayout.addWidget(self.m_pathEdit)
        btnPath = QPushButton("Path", dialog)
        btnPath.setFixedWidth(150)  # 设置固定宽度
        btnPath.clicked.connect(self.chooseExportPath)
        pathEditLayout.addWidget(btnPath)
        pathLayout.addLayout(pathEditLayout)
        return pathLayout

    def createExportScript(self, dialog):
        scriptLayout = QVBoxLayout()
        scriptLabel = QLabel("Select Export Script:", dialog)
        scriptLayout.addWidget(scriptLabel)
        self.m_scriptCombo = QComboBox(dialog)
        self.m_scriptCombo.setFixedWidth(450)  # 设置固定宽度
        self.m_scriptCombo.setEditable(False)  # 允许用户输入自定义路径
        self.m_scriptCombo.currentIndexChanged.connect(self.onScriptComboBoxChanged)
        scriptLayout.addWidget(self.m_scriptCombo)
        return scriptLayout

    def populateScriptComboBox(self):
        customFolder = os.path.join(os.getcwd(), 'custom')
        if not os.path.exists(customFolder):
            self.m_scriptCombo.clear()
            return
        if not os.path.isdir(customFolder):
            self.m_scriptCombo.clear()
            return
        for fileName in os.listdir(customFolder):
            if fileName in ['__init__.py', 'customBase.py']:
                continue
            filePath = os.path.join(customFolder, fileName)
            if not os.path.isfile(filePath):
                continue
            self.m_scriptCombo.addItem(filePath)

    def chooseExportFolder(self):
        defaultPath = os.getcwd()
        exportPath = QFileDialog.getExistingDirectory(self.m_window, "Choose Export Folder", defaultPath)
        if not exportPath:
            return
        self.m_exportFolder = exportPath
        self.m_folderEdit.setText(self.m_exportFolder)
        print("Selected Export Target:", self.m_exportFolder)

    def chooseExportPath(self):
        defaultPath = os.getcwd()
        exportPath, _ = QFileDialog.getSaveFileName(self.m_window, "Choose Export Path", defaultPath)
        if not exportPath:
            return
        self.m_exportPath = exportPath
        self.m_pathEdit.setText(self.m_exportPath)
        print("Selected Export Path:", self.m_exportPath)

    def chooseExportScript(self):
        defaultPath = os.getcwd()
        scriptPath, _ = QFileDialog.getOpenFileName(self.m_window, "Choose Export Script", defaultPath, "Python Files (*.py)")
        if not scriptPath:
            return
        self.m_exportScript = scriptPath
        self.script_line_edit.setText(self.m_exportScript)
        print("Selected Export Script:", self.m_exportScript)

    def onScriptComboBoxChanged(self, index):
        self.m_exportScript = self.m_scriptCombo.itemText(index)
        print("Selected Export Script:", self.m_exportScript)

    def doExport(self, exportPath):
        print("Do export:", exportPath)
