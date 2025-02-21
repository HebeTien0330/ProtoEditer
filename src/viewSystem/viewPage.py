'''
:@Author: tangchengqin
:@Date: 2025/1/11 12:22:52
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/13 15:59:28
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QSplitter, QTextEdit
from components.lexer import ProtoHighlighter

class ViewPage:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.setup()

    def setup(self):
        splitter: QSplitter = self.m_window.getSplitter()

        self.m_previewTextEdit = QTextEdit()
        self.m_previewTextEdit.setReadOnly(True)
        self.m_highLighter = ProtoHighlighter(self.m_previewTextEdit.document())

        splitter.addWidget(self.m_previewTextEdit)
        self.m_window.update()

    def update(self, content):
        self.m_previewTextEdit.setPlainText(content)
