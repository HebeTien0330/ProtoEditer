'''
:@Author: tangchengqin
:@Date: 2026/11/18 01:30:00
:@LastEditors: tangchengqin
:@LastEditTime: 2026/11/18 01:30:00
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class WelcomePage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_layout = QVBoxLayout()
        self.setup()
        self.setLayout(self.m_layout)

    def setup(self):
        self.m_layout.setContentsMargins(48, 36, 48, 36)
        self.m_layout.setSpacing(10)
        self.m_layout.addStretch(1)
        self.setupTitle()
        self.setupTips()
        self.m_layout.addStretch(2)

    def setupTitle(self):
        self.m_title = QLabel("协议编辑器")
        self.m_title.setObjectName("titleLabel")
        self.m_title.setAlignment(Qt.AlignLeft)
        self.m_layout.addWidget(self.m_title)
        self.m_summary = QLabel("用节点图整理 protobuf 协议，再按自定义脚本导出。")
        self.m_summary.setObjectName("mutedLabel")
        self.m_summary.setWordWrap(True)
        self.m_layout.addWidget(self.m_summary)

    def setupTips(self):
        self.m_layout.addSpacing(18)
        tips = [
            "文件 → 新建项目，或把协议目录拖到左侧文件栏。",
            "双击 .proto 打开后，在中间列表里选消息，直接改字段表。",
            "Ctrl+S 保存当前会话。文件 → 导出 会调用 custom 目录里的脚本。",
        ]
        for text in tips:
            tip = QLabel(text)
            tip.setObjectName("mutedLabel")
            tip.setWordWrap(True)
            self.m_layout.addWidget(tip)
