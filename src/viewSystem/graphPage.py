'''
:@Author: tangchengqin
:@Date: 2025/1/11 15:04:18
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 14:57:20
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QWidget, QGraphicsDropShadowEffect
from PyQt5.QtWidgets import QGraphicsRectItem, QVBoxLayout, QGraphicsTextItem, QGraphicsLineItem, QMenu
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtGui import QPen, QBrush, QColor, QWheelEvent
from PyQt5.QtCore import Qt, QRectF
from components.event import installEventSystem
from .addNodeDialog import AddNodeDialog, AddRootNodeDialog
from .editNodeDialog import EditNodeDialog

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, graphPage):
        super().__init__(scene)
        self.m_graphPage = graphPage

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
            addAction = contextMenu.addAction("Add Child Node")
            contextMenu.addSeparator()
            deleteAction = contextMenu.addAction("Delete Root Node")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == addAction:
                self.showAddNodeDialog(pos)
            elif action == deleteAction:
                self.showDeleteNodeDialog(pos)
        elif self.m_graphPage.canEditChildNode(pos):
            contextMenu = QMenu(self)
            editAction = contextMenu.addAction("Edit Child Node")
            contextMenu.addSeparator()
            moveUpAction = contextMenu.addAction("Move Up")
            contextMenu.addSeparator()
            moveDownAction = contextMenu.addAction("Move Down")
            contextMenu.addSeparator()
            deleteAction = contextMenu.addAction("Delete Node")
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
            newAction = contextMenu.addAction("New Root Node")
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
        dialog.setWindowTitle("Delete Node")
        dialog.setText("Are you sure you want to delete this node?")
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
        layout.addWidget(self.m_view)
        self.m_scene.setSceneRect(-5000, -5000, 10000, 20000)
        # 隐藏水平和垂直滚动条
        self.m_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.m_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def update(self, fileName, protos):
        self.m_fileName = fileName
        self.m_scene.clear()
        offsetX = 50
        offsetY = 50
        self.drawTree(protos, offsetX, offsetY)
        self.updateSceneRect()

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
        self.onEvent("onRefreshViews", None, "all")

    def addRootNode(self, nodeName="newField"):
        delta = {
            "fileName": self.m_fileName,
            "proto": nodeName,
        }
        self.onEvent("onAddProtoRoot", None, delta)
        self.onEvent("onRefreshViews", None, "all")

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
        self.onEvent("onRefreshViews", None, "part")

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
        self.onEvent("onRefreshViews", None, "all")

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
        self.onEvent("onRefreshViews", None, "all")

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
        self.onEvent("onRefreshViews", None, "all")

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
        if fieldType == "map":
            return QColor(255, 255, 173)  # 浅黄色
        return QColor(200, 200, 200)  # 默认浅灰色

    def createLine(self, start, end):
        line = QGraphicsLineItem(start[0], start[1], end[0], end[1])
        line.setPen(QPen(Qt.black))
        return line
