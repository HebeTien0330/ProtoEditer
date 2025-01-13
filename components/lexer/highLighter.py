'''
:@Author: tangchengqin
:@Date: 2025/1/13 15:48:48
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/13 15:58:22
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp
from pygments.token import Comment, Keyword, String, Number, Punctuation
from .lexer import ProtoLexer

# protobuf词法高亮
class ProtoHighlighter(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_highlightingRules = []
        self.init()

    def init(self):
        # 直接从 ProtoLexer.tokens 中提取规则
        tokens = (Keyword.Reserved, Keyword.Type, Keyword.Constant, Comment.Single, 
                Comment.Multiline, String, Number.Integer, Punctuation)
        for pattern, token in ProtoLexer.tokens['root']:
            if token not in tokens:
                continue
            format = QTextCharFormat()
            if token in (Keyword.Reserved, Keyword.Type):
                format.setForeground(QColor("#569CD6"))  # 蓝色关键字
                format.setFontWeight(QFont.Bold)
            elif token == Keyword.Constant:
                format.setForeground(QColor("#CE9178"))  # 橙色常量
            elif token == Comment.Single or token == Comment.Multiline:
                format.setForeground(QColor("#4CAF50"))  # 更深的绿色注释
            elif token == String:
                format.setForeground(QColor("#CE9178"))  # 橙色字符串
            elif token == Number.Integer:
                format.setForeground(QColor("#4CAF50"))  # 更深的绿色数字
            elif token == Punctuation:
                format.setForeground(QColor("#D4D4D4"))  # 浅灰色标点符号
            self.m_highlightingRules.append((QRegExp(pattern), format))

        self.multiLineCommentStartExpression = QRegExp("/\\*")
        self.multiLineCommentEndExpression = QRegExp("\\*/")
        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor("#4CAF50"))  # 更深的绿色多行注释

    def highlightBlock(self, text):
        for pattern, format in self.m_highlightingRules:
            expression = pattern
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.multiLineCommentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.multiLineCommentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.multiLineCommentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            startIndex = self.multiLineCommentStartExpression.indexIn(text, startIndex + commentLength)
