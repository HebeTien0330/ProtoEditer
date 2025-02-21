'''
:@Author: tangchengqin
:@Date: 2025/1/18 11:44:35
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 16:26:08
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QSpacerItem, QSizePolicy, QTextEdit
from components.cache import query, unpack
from components.event import installEventSystem
from .exporter import Exporter
import os

class ExportManager:

    def __init__(self, window):
        self.m_window = window
        defaultPath = os.getcwd()
        self.m_exportFolder = defaultPath
        self.m_exportPath = defaultPath
        self.m_exportScript = None
        installEventSystem(self)

    def createExportDialog(self):
        defaultTarget = query("rootPath")
        if defaultTarget:
            defaultPath = unpack(defaultTarget)
            self.m_exportFolder = defaultPath
        defaultRes = os.getcwd() + r"\example"
        if os.path.exists(defaultRes):
            self.m_exportPath = defaultRes
        dialog = QDialog(self.m_window)
        self.m_exportDialog = dialog
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
        btnExport.clicked.connect(self.doExport)
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
        folderLabel = QLabel("Select Export Target:", dialog)
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
        rootPath = query("rootPath")
        defaultPath = unpack(rootPath)
        exportPath = QFileDialog.getExistingDirectory(self.m_window, "Choose Export Target", defaultPath)
        if not exportPath:
            return
        self.m_exportFolder = exportPath
        self.m_folderEdit.setText(self.m_exportFolder)

    def chooseExportPath(self):
        defaultPath = os.getcwd()
        exportPath, _ = QFileDialog.getExistingDirectory(self.m_window, "Choose Export Path", defaultPath)
        if not exportPath:
            return
        self.m_exportPath = exportPath
        self.m_pathEdit.setText(self.m_exportPath)

    def chooseExportScript(self):
        defaultPath = os.getcwd()
        scriptPath, _ = QFileDialog.getOpenFileName(self.m_window, "Choose Export Script", defaultPath, "Python Files (*.py)")
        if not scriptPath:
            return
        self.m_exportScript = scriptPath

    def onScriptComboBoxChanged(self, index):
        scriptPath = self.m_scriptCombo.itemText(index)
        self.m_exportScript = scriptPath

    def showExportInfo(self, res=True):
        dialog = QDialog(self.m_window)
        dialog.setWindowTitle("Export Information")
        dialog.resize(200, 150)
        layout = QVBoxLayout()
        
        label = QLabel("Export completed successfully!", dialog)
        if not res:
            label = QLabel("Export fail!", dialog)
        layout.addWidget(label)
        
        btnLayout = QHBoxLayout()
        btnOk = QPushButton("OK", dialog)
        btnOk.clicked.connect(dialog.accept)
        btnLayout.addWidget(btnOk)
        
        layout.addLayout(btnLayout)
        dialog.setLayout(layout)
        dialog.exec_()

    def doExport(self):
        self.showExportInfo()
        try:
            data = {
                "exportTarget": self.m_exportFolder,
                "exportPath": self.m_exportPath,
                "exportScript": self.m_exportScript
            }
            exporter = Exporter(data)
            exporter.run()
        except:
            self.showExportInfo(False)
        finally:
            self.m_exportDialog.close()
