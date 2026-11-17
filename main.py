'''
:@Author: tangchengqin
:@Date: 2025/1/8 16:39:30
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/18 14:19:29
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplitter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from components.event import installEventSystem
from components.logger import getLogger, setLogPath
from components.cache import beginProjectCache
from src.menuBar import ManuBarManager
from src.fileSystem import FileSystem, NewFileDialog
from src.viewSystem import ViewsManager, WelcomePage
from src.newProject import NewProjectDialog
from src.exportSystem import ExportManager
from src.theme import getAppStyle
import os
import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("协议编辑器")
        self.setMinimumSize(1100, 700)
        self.resize(1440, 900)
        self.centerOnScreen()  # 调用方法使窗口居中

        # 创建主窗口内容
        self.mainContent = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainContent.setLayout(self.mainLayout)
        self.m_welcome = WelcomePage()
        self.mainLayout.addWidget(self.m_welcome)

        # 创建菜单栏
        self.m_manuBarManager = ManuBarManager(self)
        self.createMenuBar()

        # 创建文件系统
        self.m_splitter = QSplitter()
        self.m_splitter.setHandleWidth(1)
        self.m_fileSystem = FileSystem(self)
        self.m_splitter.addWidget(self.m_fileSystem.m_treeView)
        self.m_splitter.addWidget(self.mainContent)
        self.setCentralWidget(self.m_splitter)

        # 创建导出管理器
        self.m_exportManager = ExportManager(self)

        totalSize = self.size().width()
        self.m_splitter.setSizes([int(totalSize * 0.22), int(totalSize * 0.78)])

        self.m_viewsManager = ViewsManager(self)
        openedPath = self.m_fileSystem.getPath()
        if openedPath and os.path.isdir(openedPath):
            self.statusBar().showMessage(openedPath)
        else:
            self.statusBar().showMessage("尚未打开项目")

        installEventSystem(self)
        getLogger().setPersist(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save()
            return
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.m_viewsManager.focusSearch()
            return
        super().keyPressEvent(event)

    def save(self):
        self.onEvent("onSave")
        self.statusBar().showMessage("已保存", 3000)

    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     "退出",
                                     "确定要退出吗？",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No
                                    )
        if reply == QMessageBox.Yes:
            self.onEvent("onSave")
            getLogger().save()
            event.accept()
        else:
            event.ignore()

    def centerOnScreen(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2
        self.move(int(x), int(y))  # 将 x 和 y 转换为整数

    def createMenuBar(self):
        self.m_manuBarManager.addMenu('文件(F)', '新建项目 (New Project)', self.newProject)
        self.m_manuBarManager.addMenu('文件(F)', '打开项目 (Open Project)', self.openProject)
        self.m_manuBarManager.addMenu('文件(F)', '新建文件 (New File)', self.newFile)
        self.m_manuBarManager.addMenu('文件(F)', '保存 (Save)', self.saveFile)
        self.m_manuBarManager.addMenu('文件(F)', '导出 (Export)', self.export)
        self.m_manuBarManager.addMenu('文件(F)', '退出 (Exit)', self.close)

        undoAction = self.m_manuBarManager.addMenu('编辑(E)', '撤销 (Undo)')
        redoAction = self.m_manuBarManager.addMenu('编辑(E)', '重做 (Redo)')
        settingsAction = self.m_manuBarManager.addMenu('首选项(P)', '设置 (Settings)')
        undoAction.setEnabled(False)
        redoAction.setEnabled(False)
        settingsAction.setEnabled(False)

    def newProject(self):
        dialog = NewProjectDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        projectName = dialog.getProjectName().strip()
        savePath = dialog.getSavePath().strip()
        logPath = dialog.getLogPath().strip()

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
        dialog = NewFileDialog(self)
        dialog.setRootPath(self.m_fileSystem.getPath())
        if dialog.exec_() != QDialog.Accepted:
            return
        fileName = dialog.getFilePath()
        if not fileName:
            QMessageBox.warning(self, "Warning", "file name can not be empty")
            return
        self.m_fileSystem.newFile(fileName)

    def saveFile(self):
        self.save()

    def export(self):
        self.m_exportManager.createExportDialog()

    def getViewsManager(self):
        return self.m_viewsManager

    def getSplitter(self):
        return self.m_splitter

    def update(self):
        # 设置组件比例
        totalSize = self.size().width()
        self.m_splitter.setSizes([int(totalSize * 0.2), int(totalSize * 0.5), int(totalSize * 0.3)])

    def showWelcome(self):
        self.replaceMainContent(self.m_welcome)

    def replaceMainContent(self, widget):
        current = self.mainLayout.itemAt(0).widget() if self.mainLayout.count() else None
        if current is widget:
            return
        if current:
            self.mainLayout.removeWidget(current)
            current.setParent(None)
        self.mainLayout.addWidget(widget)
        self.mainContent = widget

    def createProject(self, projectName, savePath, logPath):
        if projectName.endswith(".cache"):
            projectName = projectName[:-6]
        projectDir = os.path.join(savePath, projectName)
        protoDir = os.path.join(projectDir, "proto")
        if not os.path.exists(protoDir):
            os.makedirs(protoDir)
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        cacheFile = os.path.join(projectDir, projectName + ".cache")
        beginProjectCache(cacheFile)
        setLogPath(logPath)
        self.m_fileSystem.update(protoDir)
        self.onEvent("onNewProject")
        self.setWindowTitle(f"协议编辑器  ·  {projectName}")
        self.statusBar().showMessage(protoDir)
        QMessageBox.information(self, "新建项目", f"项目已创建\n{projectDir}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("PingFang SC", 13))
    app.setStyleSheet(getAppStyle())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
