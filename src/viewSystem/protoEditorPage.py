'''
:@Author: tangchengqin
:@Date: 2026/11/18 01:45:00
:@LastEditors: tangchengqin
:@LastEditTime: 2026/11/18 01:45:00
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox
from PyQt5.QtWidgets import QPushButton, QListWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QStackedWidget, QAbstractItemView, QStyledItemDelegate
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QHeaderView, QListWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QKeySequence
from PyQt5.QtWidgets import QShortcut
from components.parser import getParser
import os
import re

SCALARS = [
    "double", "float", "int32", "int64", "uint32", "uint64", "sint32", "sint64",
    "fixed32", "fixed64", "sfixed32", "sfixed64", "bool", "string", "bytes",
]

class TypeDelegate(QStyledItemDelegate):

    def __init__(self, owner):
        super().__init__(owner.m_table)
        self.m_owner = owner

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setEditable(True)
        combo.addItems(self.m_owner.typeOptions())
        return combo

    def setEditorData(self, editor, index):
        editor.setCurrentText(index.data() or "")

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText().strip())


class FieldTable(QTableWidget):

    def __init__(self):
        super().__init__()
        self.m_owner = None
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)

    def dropEvent(self, event):
        src = self.currentRow()
        dst = self.indexAt(event.pos()).row()
        event.setDropAction(Qt.MoveAction)
        event.accept()
        if not self.m_owner:
            return
        self.m_owner.moveField(src, dst)


class ProtoEditorPage:

    def __init__(self, window):
        self.m_window = window
        self.m_preview = None
        self.m_path = ""
        self.m_doc = { "header": [], "enums": [], "messages": [] }
        self.m_text = ""
        self.m_dirty = False
        self.m_loading = False
        self.m_tab = QWidget()
        self.setup()

    def setup(self):
        self.m_layout = QVBoxLayout(self.m_tab)
        self.m_layout.setContentsMargins(12, 12, 12, 12)
        self.m_layout.setSpacing(8)
        self.setupBar()
        self.setupBody()
        shortcut = QShortcut(QKeySequence(Qt.Key_Delete), self.m_table, self.removeCurrentField)
        shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        QShortcut(QKeySequence.Find, self.m_tab, self.focusSearch)

    def setupBar(self):
        bar = QHBoxLayout()
        self.m_search = QLineEdit()
        self.m_search.setPlaceholderText("搜索消息或字段")
        self.m_search.textChanged.connect(self.onSearchChanged)
        bar.addWidget(self.m_search, 1)
        self.m_mode = QComboBox()
        self.m_mode.addItems(["消息", "枚举"])
        self.m_mode.currentIndexChanged.connect(self.onModeChanged)
        bar.addWidget(self.m_mode)
        self.m_createBtn = QPushButton("新建")
        self.m_createBtn.setObjectName("primaryButton")
        self.m_createBtn.clicked.connect(self.onCreate)
        bar.addWidget(self.m_createBtn)
        self.m_refBtn = QPushButton("引用")
        self.m_refBtn.setCheckable(True)
        self.m_refBtn.clicked.connect(self.onToggleRef)
        bar.addWidget(self.m_refBtn)
        self.m_layout.addLayout(bar)

    def setupBody(self):
        body = QHBoxLayout()
        self.m_list = QListWidget()
        self.m_list.setMinimumWidth(220)
        self.m_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.m_list.currentItemChanged.connect(self.onSymbolChanged)
        body.addWidget(self.m_list, 0)
        self.m_stack = QStackedWidget()
        self.m_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.m_table = FieldTable()
        self.m_table.m_owner = self
        self.m_table.itemChanged.connect(self.onItemChanged)
        self.m_table.setItemDelegateForColumn(2, TypeDelegate(self))
        self.m_stack.addWidget(self.m_table)
        self.m_refList = QListWidget()
        self.m_stack.addWidget(self.m_refList)
        body.addWidget(self.m_stack, 1)
        self.m_layout.addLayout(body, 1)

    def bindPreview(self, preview):
        self.m_preview = preview

    def focusSearch(self):
        self.m_search.setFocus()
        self.m_search.selectAll()

    def isMessageMode(self):
        return self.m_mode.currentIndex() == 0

    def load(self, path, content):
        self.m_path = path
        self.m_text = content
        self.m_dirty = False
        self.m_doc = getParser().scanDocument(content)
        self.reloadList()
        if self.m_preview:
            self.m_preview.update(content)
            self.revealCurrent()
        self.m_window.statusBar().showMessage(path)

    def onSearchChanged(self):
        self.reloadList()

    def symbols(self):
        if self.isMessageMode():
            return self.m_doc["messages"]
        return self.m_doc["enums"]

    def reloadList(self, selectName=None):
        if not isinstance(selectName, str):
            current = self.m_list.currentItem()
            selectName = current.text() if current else None
        keyword = self.m_search.text().strip().lower()
        self.m_list.blockSignals(True)
        self.m_list.clear()
        chosen = None
        for symbol in self.symbols():
            name = symbol["name"]
            if keyword and keyword not in name.lower() and not self.symbolHasKeyword(symbol, keyword):
                continue
            item = QListWidgetItem(name)
            self.m_list.addItem(item)
            if name == selectName:
                chosen = item
        self.m_list.blockSignals(False)
        if chosen:
            self.m_list.setCurrentItem(chosen)
            return
        if self.m_list.count() > 0:
            self.m_list.setCurrentRow(0)
            return
        self.reloadTable()

    def symbolHasKeyword(self, symbol, keyword):
        if self.isMessageMode():
            for field in symbol["fields"]:
                if keyword in field["name"].lower() or keyword in field["type"].lower():
                    return True
            return False
        for value in symbol["values"]:
            if keyword in value["name"].lower():
                return True
        return False

    def currentSymbol(self):
        item = self.m_list.currentItem()
        if not item:
            return None
        name = item.text()
        for symbol in self.symbols():
            if symbol["name"] == name:
                return symbol
        return None

    def onModeChanged(self):
        self.m_refBtn.setChecked(False)
        self.m_stack.setCurrentIndex(0)
        self.reloadList()

    def onSymbolChanged(self):
        self.reloadTable()
        if self.m_refBtn.isChecked():
            self.reloadRefs()
        self.revealCurrent()

    def revealCurrent(self):
        symbol = self.currentSymbol()
        if not symbol or not self.m_preview:
            return
        kind = "message" if self.isMessageMode() else "enum"
        self.m_preview.reveal(kind, symbol["name"])

    def reloadTable(self):
        self.m_loading = True
        symbol = self.currentSymbol()
        if self.isMessageMode():
            self.reloadMessageTable(symbol)
        else:
            self.reloadEnumTable(symbol)
        self.m_loading = False

    def reloadMessageTable(self, symbol):
        self.m_table.setColumnCount(4)
        self.m_table.setHorizontalHeaderLabels(["序号", "字段", "类型", "重复"])
        fields = []
        if symbol:
            fields = symbol["fields"]
        self.m_table.setRowCount(len(fields) + 1)
        for row, field in enumerate(fields):
            self.setTextCell(row, 0, str(field["no"]))
            self.setTextCell(row, 1, field["name"])
            self.setTextCell(row, 2, field["type"])
            self.setCheckCell(row, 3, field["isRepeated"])
        placeholder = len(fields)
        self.setTextCell(placeholder, 0, "")
        self.setTextCell(placeholder, 1, "添加字段")
        self.setTextCell(placeholder, 2, "")
        self.setTextCell(placeholder, 3, "")
        for col in range(4):
            item = self.m_table.item(placeholder, col)
            item.setForeground(QColor("#6d7488"))
            if col == 3:
                item.setFlags(Qt.ItemIsEnabled)
        header = self.m_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.m_table.setItemDelegateForColumn(2, TypeDelegate(self))

    def reloadEnumTable(self, symbol):
        self.m_table.setColumnCount(2)
        self.m_table.setHorizontalHeaderLabels(["名称", "数值"])
        values = []
        if symbol:
            values = symbol["values"]
        self.m_table.setRowCount(len(values) + 1)
        for row, value in enumerate(values):
            self.setTextCell(row, 0, value["name"])
            self.setTextCell(row, 1, str(value["no"]))
        placeholder = len(values)
        self.setTextCell(placeholder, 0, "添加取值")
        self.setTextCell(placeholder, 1, "")
        for col in range(2):
            self.m_table.item(placeholder, col).setForeground(QColor("#6d7488"))
        self.m_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def setTextCell(self, row, col, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsDragEnabled)
        self.m_table.setItem(row, col, item)

    def setCheckCell(self, row, col, checked):
        item = QTableWidgetItem("")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsDragEnabled)
        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.m_table.setItem(row, col, item)

    def isPlaceholder(self, row):
        symbol = self.currentSymbol()
        if not symbol:
            return True
        if self.isMessageMode():
            return row >= len(symbol["fields"])
        return row >= len(symbol["values"])

    def onItemChanged(self, item):
        if self.m_loading:
            return
        row = item.row()
        if self.isPlaceholder(row):
            self.commitPlaceholder(row)
            return
        if not self.applyRow(row):
            return
        self.refreshText()

    def commitPlaceholder(self, row):
        symbol = self.currentSymbol()
        if not symbol:
            return
        if self.isMessageMode():
            nameItem = self.m_table.item(row, 1)
            name = nameItem.text().strip() if nameItem else ""
            if not name or name == "添加字段":
                return
            no = 1
            if symbol["fields"]:
                no = max(field["no"] for field in symbol["fields"]) + 1
            symbol["fields"].append({
                "name": name,
                "type": "string",
                "no": no,
                "isRepeated": False,
            })
        else:
            nameItem = self.m_table.item(row, 0)
            name = nameItem.text().strip() if nameItem else ""
            if not name or name == "添加取值":
                return
            no = 0
            if symbol["values"]:
                no = max(value["no"] for value in symbol["values"]) + 1
            symbol["values"].append({ "name": name, "no": no })
        self.reloadTable()
        self.refreshText()

    def applyRow(self, row):
        symbol = self.currentSymbol()
        if not symbol:
            return False
        if self.isMessageMode():
            return self.applyMessageRow(symbol, row)
        return self.applyEnumRow(symbol, row)

    def applyMessageRow(self, symbol, row):
        noText = self.m_table.item(row, 0).text().strip()
        name = self.m_table.item(row, 1).text().strip()
        fieldType = self.m_table.item(row, 2).text().strip()
        repeated = self.m_table.item(row, 3).checkState() == Qt.Checked
        if not noText.isdigit() or not self.validName(name) or not fieldType:
            self.reloadTable()
            return False
        symbol["fields"][row] = {
            "name": name,
            "type": fieldType,
            "no": int(noText),
            "isRepeated": repeated,
        }
        return True

    def applyEnumRow(self, symbol, row):
        name = self.m_table.item(row, 0).text().strip()
        noText = self.m_table.item(row, 1).text().strip()
        if not self.validName(name) or not self.validNumber(noText):
            self.reloadTable()
            return False
        symbol["values"][row] = { "name": name, "no": int(noText) }
        return True

    def validName(self, name):
        if not name:
            return False
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            return False
        return True

    def validNumber(self, text):
        if text.startswith("-"):
            return text[1:].isdigit()
        return text.isdigit()

    def removeCurrentField(self):
        row = self.m_table.currentRow()
        symbol = self.currentSymbol()
        if row < 0 or not symbol or self.isPlaceholder(row):
            return
        if self.isMessageMode():
            del symbol["fields"][row]
        else:
            del symbol["values"][row]
        self.reloadTable()
        self.refreshText()

    def moveField(self, src, dst):
        symbol = self.currentSymbol()
        if not symbol or src < 0 or src == dst or self.isPlaceholder(src):
            self.reloadTable()
            return
        if self.isMessageMode():
            rows = symbol["fields"]
        else:
            rows = symbol["values"]
        if dst < 0 or dst >= len(rows):
            dst = len(rows) - 1
        row = rows.pop(src)
        rows.insert(dst, row)
        self.reloadTable()
        self.m_table.setCurrentCell(dst, 0)
        self.refreshText()

    def typeOptions(self):
        options = list(SCALARS)
        for enum in self.m_doc["enums"]:
            options.append(enum["name"])
        for msg in self.m_doc["messages"]:
            options.append(msg["name"])
        symbol = self.currentSymbol()
        if symbol and self.isMessageMode():
            for field in symbol["fields"]:
                if field["type"] not in options:
                    options.append(field["type"])
        return options

    def onCreate(self):
        if self.isMessageMode():
            title = "新建消息"
        else:
            title = "新建枚举"
        name, ok = QInputDialog.getText(self.m_tab, title, "名称")
        if not ok:
            return
        name = name.strip()
        if not self.validName(name):
            QMessageBox.warning(self.m_tab, title, "名称需要以字母或下划线开头。")
            return
        for symbol in self.symbols():
            if symbol["name"] == name:
                QMessageBox.warning(self.m_tab, title, "名称已存在。")
                return
        if self.isMessageMode():
            self.m_doc["messages"].append({ "name": name, "protoIdx": 0, "fields": [] })
        else:
            self.m_doc["enums"].append({ "name": name, "values": [] })
        self.reloadList(name)
        self.refreshText()

    def onToggleRef(self):
        if self.m_refBtn.isChecked():
            self.m_stack.setCurrentIndex(1)
            self.reloadRefs()
            return
        self.m_stack.setCurrentIndex(0)

    def reloadRefs(self):
        self.m_refList.clear()
        symbol = self.currentSymbol()
        if not symbol:
            return
        refs = self.collectRefs(symbol["name"])
        if not refs:
            self.m_refList.addItem("当前项目里没有其他字段引用 %s" % symbol["name"])
            return
        for text in refs:
            self.m_refList.addItem(text)

    def collectRefs(self, name):
        refs = []
        self.scanRefs(self.m_doc, self.m_path, name, refs)
        root = self.m_window.m_fileSystem.getPath()
        if not root or not os.path.isdir(root):
            return refs
        for dirpath, dirnames, fileNames in os.walk(root):
            if ".git" in dirnames:
                dirnames.remove(".git")
            for fileName in fileNames:
                if not fileName.endswith(".proto"):
                    continue
                path = os.path.join(dirpath, fileName)
                if os.path.abspath(path) == os.path.abspath(self.m_path):
                    continue
                with open(path, "r", encoding="utf-8") as file:
                    doc = getParser().scanDocument(file.read())
                self.scanRefs(doc, path, name, refs)
        return refs

    def scanRefs(self, doc, path, name, refs):
        fileName = os.path.basename(path)
        for msg in doc["messages"]:
            if msg["name"] == name and os.path.abspath(path) == os.path.abspath(self.m_path):
                continue
            for field in msg["fields"]:
                if not self.typeUses(field["type"], name):
                    continue
                prefix = ""
                if field["isRepeated"]:
                    prefix = "repeated "
                refs.append("%s    %s.%s : %s%s" % (fileName, msg["name"], field["name"], prefix, field["type"]))

    def typeUses(self, fieldType, name):
        short = name.split(".")[-1]
        parts = re.split(r'[^A-Za-z0-9_.]+', fieldType)
        for part in parts:
            if part == name or part == short or part.endswith("." + short):
                return True
        return False

    def refreshText(self):
        self.m_text = self.renderDocument()
        self.m_dirty = True
        if self.m_preview:
            self.m_preview.update(self.m_text)
            self.revealCurrent()
        self.m_window.statusBar().showMessage("未保存", 2000)

    def renderDocument(self):
        lines = list(self.m_doc["header"])
        if lines and lines[-1] != "":
            lines.append("")
        for enum in self.m_doc["enums"]:
            lines.append("enum %s {" % enum["name"])
            for value in enum["values"]:
                lines.append("  %s = %s;" % (value["name"], value["no"]))
            lines.append("}")
            lines.append("")
        for msg in self.m_doc["messages"]:
            lines.append("message %s {" % msg["name"])
            for field in msg["fields"]:
                repeated = ""
                if field["isRepeated"]:
                    repeated = "repeated "
                lines.append("  %s%s %s = %s;" % (repeated, field["type"], field["name"], field["no"]))
            lines.append("}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def saveFile(self):
        if not self.m_dirty or not self.m_path:
            return
        with open(self.m_path, "w", encoding="utf-8") as file:
            file.write(self.m_text)
        self.m_dirty = False
