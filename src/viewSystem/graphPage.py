'''
:@Author: tangchengqin
:@Date: 2025/1/11 15:04:18
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 15:44:02
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QGraphicsRectItem, QVBoxLayout, QGraphicsTextItem, QGraphicsLineItem, QMenu
from PyQt5.QtWidgets import QDialog, QMessageBox, QFrame
from PyQt5.QtGui import QPen, QBrush, QColor, QWheelEvent, QPainter, QFont
from PyQt5.QtCore import Qt, QRectF, QTimer
from components.event import installEventSystem
from .addNodeDialog import AddNodeDialog, AddRootNodeDialog
from .editNodeDialog import EditNodeDialog

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, graphPage):
        super().__init__(scene)
        self.m_graphPage = graphPage
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self.setFrameShape(QFrame.NoFrame)
        self.setBackgroundBrush(QBrush(QColor("#14161e")))
        self.setDragMode(QGraphicsView.ScrollHandDrag)

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

    def contextMenuEvent(self, event):
        pos = self.mapToScene(event.pos())
        if self.m_graphPage.canEditRootNode(pos):
            contextMenu = QMenu(self)
            addAction = contextMenu.addAction("添加字段")
            contextMenu.addSeparator()
            deleteAction = contextMenu.addAction("删除消息")
            contextMenu.addSeparator()
            moveUpAction = contextMenu.addAction("上移")
            contextMenu.addSeparator()
            moveDownAction = contextMenu.addAction("下移")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == addAction:
                self.showAddNodeDialog(pos)
            elif action == deleteAction:
                self.showDeleteNodeDialog(pos)
            elif action == moveUpAction:
                self.m_graphPage.moveRootNodeUp(pos)
            elif action == moveDownAction:
                self.m_graphPage.moveRootNodeDown(pos)
        elif self.m_graphPage.canEditChildNode(pos):
            contextMenu = QMenu(self)
            editAction = contextMenu.addAction("编辑字段")
            contextMenu.addSeparator()
            moveUpAction = contextMenu.addAction("上移")
            contextMenu.addSeparator()
            moveDownAction = contextMenu.addAction("下移")
            contextMenu.addSeparator()
            deleteAction = contextMenu.addAction("删除字段")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == editAction:
                self.showEditNodeDialog(pos)
            elif action == moveUpAction:
                self.m_graphPage.moveChildNodeUp(pos)
            elif action == moveDownAction:
                self.m_graphPage.moveChildNodeDown(pos)
            elif action == deleteAction:
                self.showDeleteNodeDialog(pos)
        else:
            contextMenu = QMenu(self)
            newAction = contextMenu.addAction("新建消息")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == newAction:
                self.showNewRootNodeDialog(pos)

    def showAddNodeDialog(self, pos):
        dialog = AddNodeDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        nodeType = dialog.getNodeType()
        nodeName = dialog.getNodeName()
        self.m_graphPage.addChildNode(pos, nodeType, nodeName)

    def showEditNodeDialog(self, pos):
        dialog = EditNodeDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        nodeType = dialog.getNodeType()
        nodeName = dialog.getNodeName()
        self.m_graphPage.editChildNode(pos, nodeType, nodeName)

    def showDeleteNodeDialog(self, pos):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("删除")
        dialog.setText("确定删除这个节点吗？")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        if dialog.exec_() != QMessageBox.Yes:
            return
        if self.m_graphPage.canEditRootNode(pos):
            self.m_graphPage.deleteRootNode(pos)
        elif self.m_graphPage.canEditChildNode(pos):
            self.m_graphPage.deleteChildNode(pos)

    def showNewRootNodeDialog(self, pos):
        dialog = AddRootNodeDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        nodeName = dialog.getNodeName()
        self.m_graphPage.addRootNode(nodeName)


class GraphPage:

    def __init__(self, window: QMainWindow):
        self.m_window = window
        self.m_tab = QWidget()
        self.m_scene = QGraphicsScene()
        self.m_view = CustomGraphicsView(self.m_scene, self)
        self.m_fileName = None
        installEventSystem(self)
        self.setup()

    def setup(self):
        self.m_tab = QWidget()
        layout = QVBoxLayout(self.m_tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.m_view)
        self.m_scene.setSceneRect(-5000, -5000, 10000, 20000)
        self.m_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def update(self, fileName, protos):
        self.m_fileName = fileName
        self.m_scene.clear()
        offsetX = 50
        offsetY = 50
        self.drawTree(protos, offsetX, offsetY)
        self.updateSceneRect()
        QTimer.singleShot(0, self.fitGraph)

    def fitGraph(self):
        bounds = self.m_scene.itemsBoundingRect().adjusted(-48, -48, 48, 48)
        if not bounds.isValid() or bounds.isEmpty():
            return
        self.m_view.resetTransform()
        self.m_view.fitInView(bounds, Qt.KeepAspectRatio)

    def updateSceneRect(self):
        allItems = self.m_scene.items()
        if not allItems:
            self.m_scene.setSceneRect(QRectF())
            return
        boundingRect = allItems[0].boundingRect()
        for item in allItems[1:]:
            reac = item.boundingRect()
            boundingRect = boundingRect.united(reac)
        margin = 100
        boundingRect.adjust(-margin, -margin, margin, margin)
        self.m_scene.setSceneRect(boundingRect)

    def createIndexText(self, index):
        return QGraphicsTextItem(index)

    def createTypeText(self, fieldType):
        return QGraphicsTextItem(fieldType)

    def createNameText(self, fieldName):
        return QGraphicsTextItem(fieldName)

    def createRectWithText(self, x, y, index, fieldType, fieldName, color, textColor=None):
        indexText = self.createIndexText(index)
        typeText = self.createTypeText(fieldType)
        nameText = self.createNameText(fieldName)
        colorForText = textColor or QColor("#1c2130")
        font = QFont("PingFang SC", 12)
        nameFont = QFont("PingFang SC", 12)
        nameFont.setWeight(QFont.DemiBold)
        for item in (indexText, typeText):
            item.setDefaultTextColor(colorForText)
            item.setFont(font)
        nameText.setDefaultTextColor(colorForText)
        nameText.setFont(nameFont)

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
        rect.setPen(QPen(QColor(255, 255, 255, 28), 1))
        rect.setFlag(QGraphicsRectItem.ItemIsMovable, False)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 90))
        shadow.setOffset(0, 6)
        rect.setGraphicsEffect(shadow)

        indexText.setPos(x + 10, y + (totalHeight - indexHeight) / 2)
        typeText.setPos(x + indexWidth + 20, y + (totalHeight - typeHeight) / 2)
        nameText.setPos(x + indexWidth + typeWidth + 30, y + (totalHeight - nameHeight) / 2)

        return rect, indexText, typeText, nameText

    def drawTree(self, protos, x, y, parent=None):
        for msgName, msgData in protos.items():
            if not isinstance(msgData, dict):
                continue

            msgRect, indexText, typeText, nameText = self.createRectWithText(
                x, y, "", "", msgName, QColor("#4c63d2"), QColor("#f5f7ff")
            )
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

    def getParentNodeText(self, parentRect):
        parentRectBounding = parentRect.sceneBoundingRect()
        parentTextItems = self.m_scene.items(parentRectBounding)
        parentText = None
        for item in parentTextItems:
            if isinstance(item, QGraphicsTextItem):
                parentText = item.toPlainText()
                break
        return parentText

    def canEditRootNode(self, pos):
        parentRect = self.findRect(pos)
        if not parentRect:
            return False
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return False
        if not (parentText.startswith("C2S") or parentText.startswith("S2C")):
            return False
        return True

    def canEditChildNode(self, pos):
        parentRect = self.findRect(pos)
        if not parentRect:
            return False
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return False
        if parentText.startswith("C2S") or parentText.startswith("S2C"):
            return False
        return True

    def addChildNode(self, pos, nodeType="newType", nodeName="newField"):
        parentRect = self.findRect(pos)
        if not parentRect:
            return
        proto = self.getParentNodeText(parentRect)
        delta = {
            "fileName": self.m_fileName,
            "proto": proto,
            "type": nodeType,
            "field": nodeName,
        }
        self.onEvent("onAddProto", None, delta)

    def addRootNode(self, nodeName="newField"):
        delta = {
            "fileName": self.m_fileName,
            "proto": nodeName,
        }
        self.onEvent("onAddProtoRoot", None, delta)

    def findRect(self, pos):
        items = self.m_scene.items(pos)
        for item in items:
            if isinstance(item, QGraphicsRectItem):
                return item
        return None

    def findChildRects(self, parentRect):
        childRects = []
        parentRectBounding = parentRect.sceneBoundingRect()
        for item in self.m_scene.items():
            if not isinstance(item, QGraphicsLineItem):
                continue
            line = item.line()
            if not parentRectBounding.contains(line.p1()):
                continue
            childRect = self.findRect(line.p2())
            if not childRect:
                continue
            childRects.append(childRect)
        childRects = childRects[::-1]
        return childRects

    def findParentRect(self, rectItem):
        rectBounding = rectItem.sceneBoundingRect()
        for item in self.m_scene.items():
            if not isinstance(item, QGraphicsLineItem):
                continue
            line = item.line()
            if not rectBounding.contains(line.p2()):
                continue
            startRect = self.findRect(line.p1())
            if not startRect:
                continue
            return startRect
        return None

    def getChildNodeTextCom(self, rectItem):
        rectBounding = rectItem.sceneBoundingRect()
        textItems = self.m_scene.items(rectBounding)
        indexText = None
        typeText = None
        nameText = None
        for item in textItems:
            if not isinstance(item, QGraphicsTextItem):
                continue
            if nameText is None:
                nameText = item
            elif typeText is None:
                typeText = item
            else:
                indexText = item
        return indexText, typeText, nameText

    def editChildNode(self, pos, nodeType, nodeName):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        indexText, typeText, nameText = self.getChildNodeTextCom(rectItem)
        if not indexText or not typeText or not nameText:
            return
        curIndex = indexText.toPlainText()
        curField = nameText.toPlainText()
        # 查找父节点
        parentRect = self.findParentRect(rectItem)
        if not parentRect:
            return
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return
        # 更新节点的类型和名称
        typeText.setPlainText(nodeType)
        nameText.setPlainText(nodeName)
        # 如果节点类型发生变化，可能需要更新颜色
        newColor = self.getFieldColor(nodeType)
        rectItem.setBrush(QBrush(newColor))
        delta = {
            "fileName": self.m_fileName,
            "proto": parentText,
            "type": nodeType,
            "field": nodeName,
            "no": curIndex,
            "oldField": curField,
        }
        self.onEvent("onEditProto", None, delta)

    def deleteChildNode(self, pos):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        indexText, typeText, nameText = self.getChildNodeTextCom(rectItem)
        if not indexText or not typeText or not nameText:
            return
        curField = nameText.toPlainText()
        parentRect = self.findParentRect(rectItem)
        if not parentRect:
            return
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return
        delta = {
            "fileName": self.m_fileName,
            "proto": parentText,
            "field": curField,
        }
        self.onEvent("onDeleteProto", None, delta)

    def deleteRootNode(self, pos):
        parentRect = self.findRect(pos)
        if not parentRect:
            return
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return
        delta = {
            "fileName": self.m_fileName,
            "proto": parentText,
        }
        self.onEvent("onDeleteProtoRoot", None, delta)

    def moveChildNodeUp(self, pos):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        parentRect = self.findParentRect(rectItem)
        if not parentRect:
            return
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return
        childRects = self.findChildRects(parentRect)
        currentIndex = childRects.index(rectItem)
        if currentIndex <= 0:
            return
        prevRect = childRects[currentIndex - 1]
        prevField = self.getParentNodeText(prevRect)
        curField = self.getParentNodeText(rectItem)
        self.swapNode(parentText, curField, prevField, "up")

    def moveChildNodeDown(self, pos):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        parentRect = self.findParentRect(rectItem)
        if not parentRect:
            return
        parentText = self.getParentNodeText(parentRect)
        if not parentText:
            return
        childRects = self.findChildRects(parentRect)
        currentIndex = childRects.index(rectItem)
        if currentIndex >= len(childRects) - 1:
            return
        nextRect = childRects[currentIndex + 1]
        nextField = self.getParentNodeText(nextRect)
        curField = self.getParentNodeText(rectItem)
        self.swapNode(parentText, curField, nextField, "down")

    def swapNode(self, proto, curField, targetField, direction):
        delta = {
            "fileName": self.m_fileName,
            "proto": proto,
            "curField": curField,
            "targetField": targetField,
            "direction": direction,
        }
        self.onEvent("onSwapProto", None, delta)

    def moveRootNodeUp(self, pos):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        parentText = self.getParentNodeText(rectItem)
        if not parentText:
            return
        self.swapRootNode(parentText, "up")

    def moveRootNodeDown(self, pos):
        rectItem = self.findRect(pos)
        if not rectItem:
            return
        parentText = self.getParentNodeText(rectItem)
        if not parentText:
            return
        self.swapRootNode(parentText, "down")

    def swapRootNode(self, proto, direction):
        delta = {
            "fileName": self.m_fileName,
            "proto": proto,
            "direction": direction,
        }
        self.onEvent("onSwapProtoRoot", None, delta)

    def getFieldColor(self, fieldType):
        if fieldType in ["double", "float"]:
            return QColor("#d3ebff")
        if fieldType in ["int32", "int64", "uint32", "uint64", "sint32", "sint64", "fixed32", "fixed64", "sfixed32", "sfixed64"]:
            return QColor("#d7f5e3")
        if fieldType == "bool":
            return QColor("#eadcfc")
        if fieldType == "string":
            return QColor("#ffd9df")
        if fieldType == "bytes":
            return QColor("#e6e8f2")
        if fieldType.startswith("map"):
            return QColor("#fff1c4")
        return QColor("#e6e8f2")

    def createLine(self, start, end):
        line = QGraphicsLineItem(start[0], start[1], end[0], end[1])
        line.setPen(QPen(QColor("#8ea0e8"), 2))
        return line
