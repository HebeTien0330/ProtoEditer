'''
:@Author: tangchengqin
:@Date: 2025/1/13 20:39:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 17:36:35
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.cache import package, unpack, save, update, query
from components.event import installEventSystem
from components.utils import getFileNameInPath
from .protoWriter import ProtoWriter
import re

class Parser:

    __isinstance = None

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def __init__(self):
        self.m_index = 1001
        self.m_protos = {}
        self.m_protoWriter = ProtoWriter()
        self.load()
        installEventSystem(self)
        self.listen("onSave", self.save)
        self.listen("onNewFile", self.onNewFile)
        self.listen("onAddProto", self.onAddProto)
        self.listen("onAddProtoRoot", self.onAddProtoRoot)
        self.listen("onEditProto", self.onEditProto)
        self.listen("onDeleteProto", self.onDeleteProto)
        self.listen("onDeleteProtoRoot", self.onDeleteProtoRoot)
        self.listen("onSwapProto", self.onSwapProto)
        self.listen("onSwapProtoRoot", self.onSwapProtoRoot)

    def save(self):
        data = {
            "index": self.m_index,
            "protos": self.m_protos
        }
        saveObj = package(data)
        update("parser", saveObj)
        save()

    def load(self):
        saveObj = query("parser")
        if not saveObj:
            return
        data: dict = unpack(saveObj)
        self.m_index = data.get("index", 1001)
        self.m_protos = data.get("protos", {})

    def splitUppercase(target):
        # 使用正则表达式找到所有大写字母及其前面的部分
        parts = re.findall('[A-Z][^A-Z]*', target)
        return parts

    def canPass(self, line):
        if not line or line == "":
            return True
        if line.startswith("//"):
            return True
        if line.startswith("/*"):
            return True
        if line.startswith("syntax"):
            return True
        if line.startswith("package"):
            return True
        if line.startswith("option"):
            return True
        return False

    def parser(self, fileName, context):
        protoData = self.m_protos.get(fileName, {})
        for line in context.splitlines():
            line = line.strip().strip(";")      # 先删除字符串两端的影响
            if self.canPass(line):
                continue
            if line.startswith("message"):
                msgName = line.split(" ")[1].strip()
                curProto = msgName
                protoData[msgName] = { "ProtoIdx": self.m_index }
                self.m_index += 1
                continue
            if line.startswith("}"):
                curProto = None
                continue
            if line.startswith("repeated"):
                _, keyType, key, _, no = line.split(" ")
                protoData[curProto][key] = { "type": keyType, "no": int(no), "isRepeated": True }
                continue
            matchStr = re.match("^map<.+>", line)
            if matchStr:
                keyType = line[:matchStr.end()]
                key, _, no = line[matchStr.end()+1:].split(" ")
                protoData[curProto][key] = { "type": keyType, "no": int(no), "isRepeated": False }
                continue

            keyType, key, _, no = line.split(" ")
            protoData[curProto][key] = { "type": keyType, "no": int(no), "isRepeated": False }
        self.m_protos[fileName] = protoData
        self.m_protoWriter.open(fileName, protoData)
        return protoData

    def getProtos(self):
        return self.m_protos

    def getProto(self, fileName, key):
        protoData = self.m_protos.get(fileName, {})
        return protoData.get(key, {})

    def onNewFile(self, filePath):
        context = self.m_protoWriter.createEmptyFile(filePath)
        self.parser(filePath, context)

    def onAddProto(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.add(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onAddProtoRoot(self, delta):
        delta["ProtoIdx"] = self.m_index
        self.m_index += 1
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.addRoot(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onEditProto(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.edit(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onDeleteProto(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.delete(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onDeleteProtoRoot(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.deleteRoot(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onSwapProto(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.swap(delta)
        self.onEvent("onRefreshViews", None, "all")

    def onSwapProtoRoot(self, delta):
        fileName = delta.get("fileName")
        if not fileName:
            return
        self.m_protos[fileName] = self.m_protoWriter.swapRoot(delta)
        self.onEvent("onRefreshViews", None, "all")


if "g_Parser" not in globals():
    global g_Parser
    g_Parser = Parser()

def getParser():
    if "g_Parser" not in globals():
        global g_Parser
        g_Parser = g_Parser()
    return g_Parser
