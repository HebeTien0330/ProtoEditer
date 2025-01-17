'''
:@Author: tangchengqin
:@Date: 2025/1/17 16:27:59
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 16:50:26
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QDialog, QLineEdit
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog
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

    def browsePath(self):
        path = QFileDialog.getExistingDirectory(self, "Choose Path", QDir.homePath())
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
