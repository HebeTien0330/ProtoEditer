'''
:@Author: tangchengqin
:@Date: 2025/1/16 15:22:26
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/16 16:59:38
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QLineEdit
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QMessageBox
import re

validTypes = [
    "double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64", 
    "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes", "map"
]

class AddNodeDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Child Node")
        self.m_layout = QVBoxLayout()
        self.setMinimumSize(300, 200)
        self.m_typeLabel = QLabel("Node Type:")
        self.m_typeComboBox = QComboBox()
        self.m_typeComboBox.addItems([
            "double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64", 
            "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes", "map"
        ])
        self.m_nameLabel = QLabel("Node Name:")
        self.m_nameLineEdit = QLineEdit()
        self.m_btnSubmit = QPushButton("Submit")
        self.m_btnSubmit.clicked.connect(self.onSubmitClicked)
        self.m_layout.addWidget(self.m_typeLabel)
        self.m_layout.addWidget(self.m_typeComboBox)
        self.m_layout.addWidget(self.m_nameLabel)
        self.m_layout.addWidget(self.m_nameLineEdit)
        self.m_layout.addWidget(self.m_btnSubmit)
        self.setLayout(self.m_layout)

    def getNodeType(self):
        return self.m_typeComboBox.currentText()

    def getNodeName(self):
        return self.m_nameLineEdit.text()
    
    def onSubmitClicked(self):
        nodeType = self.getNodeType()
        if not self.validTypeInput(nodeType):
            QMessageBox.warning(self, "Invalid Input", "Node type error!!!")
            return
        nodeName = self.getNodeName()
        if not nodeName:
            QMessageBox.warning(self, "Invalid Input", "Node name error!!!")
            return
        self.accept()

    def validTypeInput(self, nodeType):
        if not nodeType:
            return False
        if nodeType not in validTypes:
            return False
        return True

    def validNameInput(self, nodeName):
        if not nodeName:
            return False
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', nodeName):
            return False
        return True
