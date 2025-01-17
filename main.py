'''
:@Author: tangchengqin
:@Date: 2025/1/8 16:39:30
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/16 18:10:30
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplitter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from components.event import installEventSystem
from src.menuBar import ManuBarManager
from src.fileSystem import FileSystem
from src.viewSystem import ViewsManager
from src.newProject import NewProjectDialog
import sys

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
        self.m_splitter = QSplitter()
        self.m_fileSystem = FileSystem(self)
        self.m_splitter.addWidget(self.m_fileSystem.m_treeView)
        self.m_splitter.addWidget(self.mainContent)
        self.setCentralWidget(self.m_splitter)

        totalSize = self.size().width()
        self.m_splitter.setSizes([int(totalSize * 0.2), int(totalSize * 0.8)])

        #创建展示界面
        self.m_viewsManager = ViewsManager(self)

        installEventSystem(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save()
        else:
            super().keyPressEvent(event)

    def save(self):
        self.onEvent("onSave")
        print("all save!")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 
                                     'Message', "Are you sure to quit?", 
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No
                                    )
        if reply == QMessageBox.Yes:
            self.onEvent("onSave")
            event.accept()
        else:
            event.ignore()

    def centerOnScreen(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(int(x), int(y))  # 将 x 和 y 转换为整数

    def createMenuBar(self):
        # 添加文件菜单
        self.m_manuBarManager.addMenu('文件(F)', '新建项目 (New Project)', self.newProject)
        self.m_manuBarManager.addMenu('文件(F)', '打开项目 (Open Project)', self.openProject)
        self.m_manuBarManager.addMenu('文件(F)', '新建文件 (New File)', self.newFile)
        self.m_manuBarManager.addMenu('文件(F)', '保存 (Save)', self.saveFile)
        self.m_manuBarManager.addMenu('文件(F)', '导出 (Export)', self.export)
        self.m_manuBarManager.addMenu('文件(F)', '退出 (Exit)', self.close)

        # 添加编辑菜单
        self.m_manuBarManager.addMenu('编辑(E)', '撤销 (Undo)')
        self.m_manuBarManager.addMenu('编辑(E)', '重做 (Redo)')

        # 添加首选项菜单
        self.m_manuBarManager.addMenu('首选项(P)', '设置 (Settings)')

    def newProject(self):
        dialog = NewProjectDialog(self)
        if dialog.exec_() != QDialogButtonBox.Ok:
            return
        projectName = dialog.getProjectName()
        savePath = dialog.getSavePath()
        logPath = dialog.getLogPath()

        # 验证输入
        if not projectName:
            QMessageBox.warning(self, "警告", "项目名称不能为空")
            return
        if not savePath:
            QMessageBox.warning(self, "警告", "保存路径不能为空")
            return
        if not logPath:
            QMessageBox.warning(self, "警告", "日志路径不能为空")
            return

        # 处理新建项目逻辑
        self.createProject(projectName, savePath, logPath)

    def openProject(self):
        self.onEvent("onOpenFile")

    def newFile(self):
        pass

    def saveFile(self):
        QMessageBox.information(self, "保存(S)", "保存文件")

    def export(self):
        pass

    def getViewsManager(self):
        return self.m_viewsManager

    def getSplitter(self):
        return self.m_splitter

    def update(self):
        # 设置组件比例
        totalSize = self.size().width()
        self.m_splitter.setSizes([int(totalSize * 0.2), int(totalSize * 0.5), int(totalSize * 0.3)])

    def replaceMainContent(self, widget):
        layoutCnt = self.mainLayout.count()
        if layoutCnt > 1:
            old_widget = self.mainLayout.itemAt(1).widget()
            self.mainLayout.removeWidget(old_widget)
            old_widget.setParent(None)
        self.mainLayout.insertWidget(1, widget)
        self.mainContent = widget

    def createProject(self, projectName, savePath, logPath):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
