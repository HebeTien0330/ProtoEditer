'''
:@Author: tangchengqin
:@Date: 2025/1/17 16:27:59
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 17:11:00
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QDialog, QLineEdit
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QDir

class NewFileDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建文件")
        self.resize(460, 240)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 18, 20, 18)
        self.layout.setSpacing(8)
        self.label = QLabel("文件名")
        self.label.setObjectName("panelTitle")
        self.layout.addWidget(self.label)
        self.fileNameLineEdit = QLineEdit()
        self.fileNameLineEdit.setPlaceholderText("login.proto")
        self.layout.addWidget(self.fileNameLineEdit)
        self.pathLabel = QLabel("目录")
        self.pathLabel.setObjectName("panelTitle")
        self.layout.addWidget(self.pathLabel)
        self.pathLineEdit = QLineEdit()
        self.layout.addWidget(self.pathLineEdit)
        self.browseButton = QPushButton("浏览")
        self.browseButton.clicked.connect(self.browsePath)
        self.layout.addWidget(self.browseButton)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        okButton.setObjectName("primaryButton")
        okButton.setText("创建")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.m_path = None

    def setRootPath(self, path):
        self.m_path = path

    def browsePath(self):
        rootPath = self.m_path
        if not self.m_path:
            rootPath = QDir.homePath()
        path = QFileDialog.getExistingDirectory(self, "Choose Path", rootPath)
        if not path:
            return
        self.pathLineEdit.setText(path)

    def getFilePath(self):
        fileName = self.fileNameLineEdit.text()
        if not fileName:
            return None
        if not fileName.endswith(".proto"):
            fileName += ".proto"
        path = self.pathLineEdit.text()
        if not path:
            return None
        return QDir.toNativeSeparators(f"{path}/{fileName}")

    def accept(self):
        filePath = self.getFilePath()
        if not filePath:
            QMessageBox.warning(self, "无法创建", "请填写文件名和目录。")
            return
        if QDir(filePath).exists():
            QMessageBox.warning(self, "文件已存在", f"{filePath} 已经存在。")
            return
        super().accept()
