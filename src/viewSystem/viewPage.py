'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:22:52
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/13 15:59:28
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QSplitter, QTextEdit, QWidget, QVBoxLayout, QLabel
from components.lexer import ProtoHighlighter

class ViewPage:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.setup()

    def setup(self):
        splitter: QSplitter = self.m_window.getSplitter()

        self.m_panel = QWidget()
        self.m_layout = QVBoxLayout(self.m_panel)
        self.m_layout.setContentsMargins(12, 12, 12, 12)
        self.m_layout.setSpacing(8)
        self.m_title = QLabel("源码预览")
        self.m_title.setObjectName("panelTitle")
        self.m_layout.addWidget(self.m_title)

        self.m_previewTextEdit = QTextEdit()
        self.m_previewTextEdit.setReadOnly(True)
        self.m_previewTextEdit.setPlaceholderText("打开协议文件后，这里显示源码")
        self.m_highLighter = ProtoHighlighter(self.m_previewTextEdit.document())
        self.m_layout.addWidget(self.m_previewTextEdit)

        splitter.addWidget(self.m_panel)
        self.m_window.update()

    def update(self, content):
        self.m_previewTextEdit.setPlainText(content)

    def reveal(self, kind, name):
        if kind == "enum":
            keyword = "enum %s" % name
        else:
            keyword = "message %s" % name
        document = self.m_previewTextEdit.document()
        cursor = document.find(keyword)
        if cursor.isNull():
            return
        self.m_previewTextEdit.setTextCursor(cursor)
        self.m_previewTextEdit.ensureCursorVisible()
