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
        self.setWindowTitle("NewFile")
        self.layout = QVBoxLayout()
        self.label = QLabel("File Name:")
        self.layout.addWidget(self.label)
        self.fileNameLineEdit = QLineEdit()
        self.layout.addWidget(self.fileNameLineEdit)
        self.pathLabel = QLabel("Path:")
        self.layout.addWidget(self.pathLabel)
        self.pathLineEdit = QLineEdit()
        self.layout.addWidget(self.pathLineEdit)
        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.browsePath)
        self.layout.addWidget(self.browseButton)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
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
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid file name and path.")
            return
        if QDir(filePath).exists():
            QMessageBox.warning(self, "File Exists", f"The file '{filePath}' already exists.")
            return
        super().accept()
