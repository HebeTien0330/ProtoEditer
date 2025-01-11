'''
:@Author: tangchengqin
:@Date: 2025/1/11 17:00:15
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 17:28:40
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton, QFileDialog, QDialogButtonBox, QApplication
from PyQt5.QtCore import Qt
import os

class NewProjectDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建项目")
        self.setGeometry(100, 100, 500, 300)  # 增加对话框的宽度和高度
        self.m_layout = QVBoxLayout()
        self.setup()
        self.setLayout(self.m_layout)
        self.centerOnScreen()

    def setup(self):
        self.setupProjectName()
        self.setupSavePath()
        self.setupLogPath()
        self.setupConfirm()

    def setupProjectName(self):
        self.m_ProjectName = QLabel("项目名称:")
        self.m_layout.addWidget(self.m_ProjectName)
        self.m_projectNameEditer = QLineEdit()
        self.m_layout.addWidget(self.m_projectNameEditer)
        self.m_projectNameEditer.setText("NewProject.pkl")

    def setupSavePath(self):
        self.m_savePath = QLabel("保存路径:")
        self.m_layout.addWidget(self.m_savePath)
        self.m_savePathLayout = QHBoxLayout()
        self.m_savePathEditer = QLineEdit()
        self.m_savePathLayout.addWidget(self.m_savePathEditer)
        self.m_btnBrowseSave = QPushButton("浏览")
        self.m_btnBrowseSave.clicked.connect(self.browseSavePath)
        self.m_savePathLayout.addWidget(self.m_btnBrowseSave)
        self.m_layout.addLayout(self.m_savePathLayout)
        # 设置默认保存路径
        defaultSavePath = os.path.abspath("./cachefiles")
        self.m_savePathEditer.setText(defaultSavePath)

    def setupLogPath(self):
        self.m_logPath = QLabel("日志路径:")
        self.m_layout.addWidget(self.m_logPath)
        self.m_logPathLayout = QHBoxLayout()
        self.m_logPathEditer = QLineEdit()
        self.m_logPathLayout.addWidget(self.m_logPathEditer)
        self.m_btnBrowseLog = QPushButton("浏览")
        self.m_btnBrowseLog.clicked.connect(self.browseLogPath)
        self.m_logPathLayout.addWidget(self.m_btnBrowseLog)
        self.m_layout.addLayout(self.m_logPathLayout)
        # 设置默认日志路径
        defaultLogPath = os.path.abspath("./log")
        self.m_logPathEditer.setText(defaultLogPath)

    def setupConfirm(self):
        # 确认和取消按钮
        self.m_btnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.m_btnBox.accepted.connect(self.accept)
        self.m_btnBox.rejected.connect(self.reject)

        # 创建一个水平布局来放置按钮框
        btnLayout = QHBoxLayout()

        # 获取按钮框中的按钮
        ok_button = self.m_btnBox.button(QDialogButtonBox.Ok)
        cancel_button = self.m_btnBox.button(QDialogButtonBox.Cancel)

        # 创建一个水平布局来放置按钮和间距
        btnLayout.addWidget(ok_button)
        btnLayout.addSpacing(30)  # 添加固定间距
        btnLayout.addWidget(cancel_button)

        # 将水平布局添加到主布局中
        self.m_layout.addLayout(btnLayout)

    def centerOnScreen(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(int(x), int(y))  # 将 x 和 y 转换为整数

    def browseSavePath(self):
        path = QFileDialog.getExistingDirectory(self, "选择保存路径", self.m_savePathEditer.text())
        if not path:
            return
        self.m_savePathEditer.setText(path)

    def browseLogPath(self):
        path = QFileDialog.getExistingDirectory(self, "选择日志路径", self.m_logPathEditer.text())
        if not path:
            return
        self.m_logPathEditer.setText(path)

    def getProjectName(self):
        return self.m_projectNameEditer.text()

    def getSavePath(self):
        return self.m_savePathEditer.text()

    def getLogPath(self):
        return self.m_logPathEditer.text()
