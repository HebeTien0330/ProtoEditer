'''
:@Author: tangchengqin
:@Date: 2025/1/8 16:39:30
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/8 16:39:30
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplitter
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from components.event import installEventSystem
from src.menuBar import ManuBarManager
from src.fileSystem import FileSystem

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("协议编辑器")
        self.setGeometry(100, 100, 1920, 1080)  # 设置初始位置和大小
        self.centerOnScreen()  # 调用方法使窗口居中

        # 创建主窗口内容
        self.mainContent = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainContent.setLayout(self.mainLayout)

        # 创建菜单栏
        self.m_manuBarManager = ManuBarManager(self)
        self.createMenuBar()

        # 创建文件系统
        splitter = QSplitter()
        self.m_fileSystem = FileSystem(self)
        splitter.addWidget(self.m_fileSystem.m_treeView)
        splitter.addWidget(self.mainContent)
        self.setCentralWidget(splitter)

        # 设置拉伸因子，使文件系统组件的宽度较小
        splitter.setStretchFactor(0, 1)  # 文件系统组件
        splitter.setStretchFactor(1, 50)  # 主窗口内容

        installEventSystem(self)

    def centerOnScreen(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(int(x), int(y))  # 将 x 和 y 转换为整数

    def createMenuBar(self):
        # 添加文件菜单
        self.m_manuBarManager.addMenu('文件(F)', '新建(N)', self.newFile)
        self.m_manuBarManager.addMenu('文件(F)', '打开(O)', self.openFile)
        self.m_manuBarManager.addMenu('文件(F)', '保存(S)', self.saveFile)
        self.m_manuBarManager.addMenu('文件(F)', '退出(D)', self.close)

        # 添加编辑菜单
        self.m_manuBarManager.addMenu('编辑(E)', '撤销(Z)')
        self.m_manuBarManager.addMenu('编辑(E)', '重做(Y)')

        # 添加首选项菜单
        self.m_manuBarManager.addMenu('首选项(P)', '设置')

    def newFile(self):
        QMessageBox.information(self, "新建(N)", "新建文件")

    def openFile(self):
        self.onEvent("onOpenFile")

    def saveFile(self):
        QMessageBox.information(self, "保存(S)", "保存文件")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
