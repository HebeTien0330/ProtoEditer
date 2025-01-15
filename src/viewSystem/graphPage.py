'''
:@Author: tangchengqin
:@Date: 2025/1/11 15:04:18
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/15 17:32:25
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QGraphicsRectItem, QVBoxLayout, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtGui import QPen, QBrush, QColor, QWheelEvent
from PyQt5.QtCore import Qt

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

    def calcZoomFactor(self, event):
        zoomFactor = 1.25
        if event.angleDelta().y() < 0:
            zoomFactor = 1 / zoomFactor
        return zoomFactor

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            zoomFactor = self.calcZoomFactor(event)
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
            self.scale(zoomFactor, zoomFactor)
        elif event.modifiers() & Qt.ShiftModifier:
            # 按住 Shift 键进行横向滚动
            delta = event.angleDelta().y()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta)
        else:
            super().wheelEvent(event)


class GraphPage:
    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_tab = QWidget()
        self.m_scene = QGraphicsScene()
        self.m_view = CustomGraphicsView(self.m_scene)
        self.setup()

    def setup(self):
        self.m_tab = QWidget()
        layout = QVBoxLayout(self.m_tab)
        layout.addWidget(self.m_view)
        self.m_scene.setSceneRect(-5000, -5000, 10000, 20000)       # TODO: 有办法自适应吗？
        # 隐藏水平和垂直滚动条
        self.m_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def update(self, protos):
        self.m_scene.clear()
        offsetX = 50
        offsetY = 50
        self.drawTree(protos, offsetX, offsetY)

    def createIndexText(self, index):
        return QGraphicsTextItem(index)

    def createTypeText(self, fieldType):
        return QGraphicsTextItem(fieldType)

    def createNameText(self, fieldName):
        return QGraphicsTextItem(fieldName)

    def createRectWithText(self, x, y, index, fieldType, fieldName, color):
        indexText = self.createIndexText(index)
        typeText = self.createTypeText(fieldType)
        nameText = self.createNameText(fieldName)

        indexRect = indexText.boundingRect()
        typeRect = typeText.boundingRect()
        nameRect = nameText.boundingRect()

        indexWidth, indexHeight = indexRect.width(), indexRect.height()
        typeWidth, typeHeight = typeRect.width(), typeRect.height()
        nameWidth, nameHeight = nameRect.width(), nameRect.height()

        totalWidth = indexWidth + typeWidth + nameWidth + 60
        totalHeight = max(indexHeight, typeHeight, nameHeight) + 20

        rect = QGraphicsRectItem(x, y, totalWidth, totalHeight)
        rect.setBrush(QBrush(color))
        rect.setPen(QPen(Qt.black))
        rect.setFlag(QGraphicsRectItem.ItemIsMovable, False)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)  # 设置模糊半径
        shadow.setColor(QColor(0, 0, 0, 128))  # 设置阴影颜色和透明度
        shadow.setOffset(4, 4)  # 设置阴影偏移量
        rect.setGraphicsEffect(shadow)

        indexText.setPos(x + 10, y + (totalHeight - indexHeight) / 2)
        typeText.setPos(x + indexWidth + 20, y + (totalHeight - typeHeight) / 2)
        nameText.setPos(x + indexWidth + typeWidth + 30, y + (totalHeight - nameHeight) / 2)

        return rect, indexText, typeText, nameText

    def drawTree(self, protos, x, y, parent=None):
        for msgName, msgData in protos.items():
            if not isinstance(msgData, dict):
                continue

            msgRect, indexText, typeText, nameText = self.createRectWithText(x, y, "", "", msgName, QColor(200, 200, 200))
            self.m_scene.addItem(msgRect)
            self.m_scene.addItem(indexText)
            self.m_scene.addItem(typeText)
            self.m_scene.addItem(nameText)

            rect = msgRect.rect()
            width = rect.width()
            height = rect.height()
            if parent:
                line = self.createLine(parent, (x + width, y + height / 2))
                self.m_scene.addItem(line)

            # self.createSubNode(x, y, width, msgData, msgRect)
            subX = x + width + 30
            subY = y
            index = 1
            maxSubHeight = 0
            lastSubY = subY
            for fieldName, fieldInfo in msgData.items():
                if fieldName == "ProtoIdx":
                    continue
                fieldType = fieldInfo['type']
                fieldColor = self.getFieldColor(fieldType)
                subRect, subIndexText, subTypeText, subNameText = self.createRectWithText(subX, subY, str(index), fieldType, fieldName, fieldColor)
                self.m_scene.addItem(subRect)
                self.m_scene.addItem(subIndexText)
                self.m_scene.addItem(subTypeText)
                self.m_scene.addItem(subNameText)

                msgWidth = msgRect.rect().width()
                msgHeight = msgRect.rect().height()
                subWidth = subRect.rect().width()
                subHeight = subRect.rect().height()
                line = self.createLine((x + msgWidth, y + msgHeight / 2), (subX, subY + subHeight / 2))
                self.m_scene.addItem(line)

                self.drawTree(fieldInfo, subX + subWidth + 30, subY, (subX + subWidth, subY + subHeight / 2))

                subY += subHeight + 50
                maxSubHeight = max(maxSubHeight, subHeight)
                index += 1
                lastSubY = subY

            subY = lastSubY + maxSubHeight + 50
            y = subY

    def getFieldColor(self, fieldType):
        if fieldType in ["double", "float"]:
            return QColor(173, 216, 230)  # 浅蓝色
        if fieldType in ["int32", "int64", "uint32", "uint64", "sint32", "sint64", "fixed32", "fixed64", "sfixed32", "sfixed64"]:
            return QColor(173, 255, 173)  # 浅绿色
        if fieldType == "bool":
            return QColor(216, 173, 230)  # 浅紫色
        if fieldType == "string":
            return QColor(255, 173, 173)  # 浅红色
        if fieldType == "bytes":
            return QColor(200, 200, 200)  # 浅灰色
        return QColor(200, 200, 200)  # 默认浅灰色

    def createLine(self, start, end):
        line = QGraphicsLineItem(start[0], start[1], end[0], end[1])
        line.setPen(QPen(Qt.black))
        return line
