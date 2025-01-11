'''
:@Author: tangchengqin
:@Date: 2025/1/11 15:04:18
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 15:04:18
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QWidget, QGraphicsRectItem, QVBoxLayout

class GraphPage:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_tab = QWidget()
        self.m_scene = QGraphicsScene()
        self.m_view = QGraphicsView(self.m_scene)
        self.setup()

    def setup(self):
        # 添加一个可拖动的矩形
        rect = QGraphicsRectItem(0, 0, 100, 100)
        rect.setFlag(QGraphicsRectItem.ItemIsMovable)  # 设置可移动标志
        self.m_scene.addItem(rect)

        # 创建一个 QWidget 作为 GraphPage 的内容部件
        self.m_tab = QWidget()
        layout = QVBoxLayout(self.m_tab)
        layout.addWidget(self.m_view)

    def update(self, content):
        pass
