'''
:@Author: tangchengqin
:@Date: 2025/1/18 11:44:35
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 16:26:08
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QTextEdit
from PyQt5.QtGui import QTextCursor
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
        self.m_logEdit = None
        self.m_statusLabel = None
        installEventSystem(self)
        self.listen("onAppendExportInfo", self.onAppendExportInfo)

    def createExportDialog(self):
        defaultTarget = query("rootPath")
        if defaultTarget:
            self.m_exportFolder = unpack(defaultTarget)
        defaultRes = os.path.join(os.getcwd(), "example")
        if os.path.isdir(defaultRes):
            self.m_exportPath = defaultRes
        dialog = QDialog(self.m_window)
        self.m_exportDialog = dialog
        dialog.setWindowTitle("导出")
        dialog.resize(680, 520)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        # 选择协议目录、导出目录和脚本
        layout.addLayout(self.createExportFolder(dialog))
        layout.addLayout(self.createExportPath(dialog))
        layout.addLayout(self.createExportScript(dialog))
        self.populateScriptComboBox()

        self.m_statusLabel = QLabel("选择目录和脚本后开始导出", dialog)
        self.m_statusLabel.setObjectName("mutedLabel")
        layout.addWidget(self.m_statusLabel)

        self.m_logEdit = QTextEdit(dialog)
        self.m_logEdit.setReadOnly(True)
        self.m_logEdit.setPlaceholderText("导出日志会显示在这里")
        layout.addWidget(self.m_logEdit, 1)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)
        self.m_btnExport = QPushButton("导出", dialog)
        self.m_btnExport.setObjectName("primaryButton")
        self.m_btnExport.clicked.connect(self.doExport)
        btnClose = QPushButton("关闭", dialog)
        btnClose.clicked.connect(dialog.reject)
        btnLayout.addWidget(self.m_btnExport)
        btnLayout.addWidget(btnClose)
        layout.addLayout(btnLayout)
        dialog.exec_()

    def createExportFolder(self, dialog):
        folderLayout = QVBoxLayout()
        folderLayout.setSpacing(6)
        folderLabel = QLabel("协议目录", dialog)
        folderLabel.setObjectName("panelTitle")
        folderLayout.addWidget(folderLabel)
        folderEditLayout = QHBoxLayout()
        self.m_folderEdit = QLineEdit(self.m_exportFolder, dialog)
        folderEditLayout.addWidget(self.m_folderEdit, 1)
        btnFolder = QPushButton("浏览", dialog)
        btnFolder.clicked.connect(self.chooseExportFolder)
        folderEditLayout.addWidget(btnFolder)
        folderLayout.addLayout(folderEditLayout)
        return folderLayout

    def createExportPath(self, dialog):
        pathLayout = QVBoxLayout()
        pathLayout.setSpacing(6)
        pathLabel = QLabel("导出到", dialog)
        pathLabel.setObjectName("panelTitle")
        pathLayout.addWidget(pathLabel)
        pathEditLayout = QHBoxLayout()
        self.m_pathEdit = QLineEdit(self.m_exportPath, dialog)
        pathEditLayout.addWidget(self.m_pathEdit, 1)
        btnPath = QPushButton("浏览", dialog)
        btnPath.clicked.connect(self.chooseExportPath)
        pathEditLayout.addWidget(btnPath)
        pathLayout.addLayout(pathEditLayout)
        return pathLayout

    def createExportScript(self, dialog):
        scriptLayout = QVBoxLayout()
        scriptLayout.setSpacing(6)
        scriptLabel = QLabel("导出脚本", dialog)
        scriptLabel.setObjectName("panelTitle")
        scriptLayout.addWidget(scriptLabel)
        self.m_scriptCombo = QComboBox(dialog)
        self.m_scriptCombo.currentIndexChanged.connect(self.onScriptComboBoxChanged)
        scriptLayout.addWidget(self.m_scriptCombo)
        return scriptLayout

    def populateScriptComboBox(self):
        self.m_scriptCombo.clear()
        customFolder = os.path.join(os.getcwd(), "custom")
        if not os.path.isdir(customFolder):
            return
        for fileName in sorted(os.listdir(customFolder)):
            if fileName in ["__init__.py", "customBase.py"] or not fileName.endswith(".py"):
                continue
            filePath = os.path.join(customFolder, fileName)
            if os.path.isfile(filePath):
                self.m_scriptCombo.addItem(fileName, filePath)

    def chooseExportFolder(self):
        rootPath = query("rootPath")
        defaultPath = unpack(rootPath) if rootPath else os.getcwd()
        exportPath = QFileDialog.getExistingDirectory(self.m_window, "选择协议目录", defaultPath)
        if not exportPath:
            return
        self.m_exportFolder = exportPath
        self.m_folderEdit.setText(self.m_exportFolder)

    def chooseExportPath(self):
        exportPath = QFileDialog.getExistingDirectory(self.m_window, "选择导出目录", self.m_exportPath or os.getcwd())
        if not exportPath:
            return
        self.m_exportPath = exportPath
        self.m_pathEdit.setText(self.m_exportPath)

    def onScriptComboBoxChanged(self, index):
        if index < 0:
            self.m_exportScript = None
            return
        self.m_exportScript = self.m_scriptCombo.itemData(index)

    def onAppendExportInfo(self, text):
        self.appendLog(text)

    def appendLog(self, text):
        if not self.m_logEdit:
            return
        self.m_logEdit.moveCursor(QTextCursor.End)
        self.m_logEdit.insertPlainText(text)
        self.m_logEdit.ensureCursorVisible()

    def doExport(self):
        self.m_exportFolder = self.m_folderEdit.text().strip()
        self.m_exportPath = self.m_pathEdit.text().strip()
        self.m_logEdit.clear()
        self.m_statusLabel.setText("正在导出…")
        self.m_btnExport.setEnabled(False)
        res = True
        try:
            data = {
                "exportTarget": self.m_exportFolder,
                "exportPath": self.m_exportPath,
                "exportScript": self.m_exportScript
            }
            exporter = Exporter(data)
            exporter.run()
        except Exception as exc:
            res = False
            self.appendLog(f"\n{exc}\n")
            self.m_statusLabel.setText("导出失败")
        if res:
            self.appendLog("\n导出完成。\n")
            self.m_statusLabel.setText("导出完成")
        self.m_btnExport.setEnabled(True)
