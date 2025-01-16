'''
:@Author: tangchengqin
:@Date: 2025/1/13 20:39:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/16 17:19:18
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.cache import package, unpack, save, update, query
from components.event import installEventSystem
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
        self.protoWriter = ProtoWriter()
        self.load()
        installEventSystem(self)
        self.listen("save", self.save)
        self.listen("onChangeProto", self.onChangeProto)
        self.listen("onEditProto", self.onEditProto)

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
        curProto = None
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
        self.protoWriter.open(fileName, protoData)
        return protoData

    def getProtos(self):
        return self.m_protos
    def getProto(self, fileName, key):
        protoData = self.m_protos.get(fileName, {})
        return protoData.get(key, {})

    def onChangeProto(self, delta):
        self.protoWriter.update(delta)

    def onEditProto(self, delta):
        self.protoWriter.edit(delta)


if "g_Parser" not in globals():
    global g_Parser
    g_Parser = Parser()

def getParser():
    if "g_Parser" not in globals():
        global g_Parser
        g_Parser = g_Parser()
    return g_Parser
