'''
:@Author: tangchengqin
:@Date: 2025/1/16 16:43:37
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/16 16:43:37
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

class EditNodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("编辑字段")
        self.m_layout = QVBoxLayout()
        self.m_layout.setContentsMargins(20, 18, 20, 18)
        self.m_layout.setSpacing(8)
        self.setMinimumSize(320, 220)
        self.m_typeLabel = QLabel("类型")
        self.m_typeLabel.setObjectName("panelTitle")
        self.m_typeComboBox = QComboBox()
        self.m_typeComboBox.addItems([
            "double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64", 
            "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes", "map"
        ])
        self.m_nameLabel = QLabel("字段名")
        self.m_nameLabel.setObjectName("panelTitle")
        self.m_nameLineEdit = QLineEdit()
        self.m_btnSubmit = QPushButton("保存")
        self.m_btnSubmit.setObjectName("primaryButton")
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
            QMessageBox.warning(self, "类型无效", "请选择字段类型。")
            return
        nodeName = self.getNodeName()
        if not self.validNameInput(nodeName):
            QMessageBox.warning(self, "名称无效", "字段名需要以字母或下划线开头。")
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
