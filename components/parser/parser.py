'''
:@Author: tangchengqin
:@Date: 2025/1/13 20:39:58
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 10:04:43
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
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
        self.m_documents = {}
        self.m_protoWriter = ProtoWriter()
        installEventSystem(self)
        self.listen("onDeleteFile", self.onDeleteFile)
        self.listen("onNewFile", self.onNewFile)
        self.listen("onAddProto", self.onAddProto)
        self.listen("onAddProtoRoot", self.onAddProtoRoot)
        self.listen("onEditProto", self.onEditProto)
        self.listen("onDeleteProto", self.onDeleteProto)
        self.listen("onDeleteProtoRoot", self.onDeleteProtoRoot)
        self.listen("onSwapProto", self.onSwapProto)
        self.listen("onSwapProtoRoot", self.onSwapProtoRoot)

    def reset(self):
        self.m_index = 1001
        self.m_protos = {}
        self.m_documents = {}
        self.m_protoWriter.reset()

    def splitUppercase(target):
        # 使用正则表达式找到所有大写字母及其前面的部分
        parts = re.findall('[A-Z][^A-Z]*', target)
        return parts

    def canPass(self, line):
        if not line or line == "":
            return True
        if line.startswith("//"):
            return True
        if line.startswith("/*") or line.startswith("*") or line.startswith("*/"):
            return True
        if line.startswith("syntax"):
            return True
        if line.startswith("package"):
            return True
        if line.startswith("option"):
            return True
        if line.startswith("import"):
            return True
        return False

    def cleanLine(self, line):
        line = line.strip()
        if "//" in line:
            line = line.split("//", 1)[0]
        return line.strip().strip(";")

    def parser(self, fileName, context):
        doc = self.scanDocument(context)
        self.m_documents[fileName] = doc
        protoData = self.toProtoData(doc)
        self.m_protos[fileName] = protoData
        self.m_protoWriter.open(fileName, protoData)
        return protoData

    def scanDocument(self, context):
        header = []
        enums = []
        messages = []
        started = False
        inEnum = None
        inMessage = None
        for rawLine in context.splitlines():
            line = self.cleanLine(rawLine)
            if not started:
                if line.startswith("message") or line.startswith("enum ") or line.startswith("enum{"):
                    started = True
                else:
                    header.append(rawLine)
                    continue
            if line.startswith("enum ") or line.startswith("enum{"):
                enumName = line.split()[1].strip("{")
                inEnum = { "name": enumName, "values": [] }
                enums.append(inEnum)
                inMessage = None
                if "{" in line and line.endswith("}"):
                    inEnum = None
                continue
            if line.startswith("message"):
                msgName = line.split()[1].strip("{")
                inMessage = { "name": msgName, "protoIdx": self.m_index, "fields": [] }
                self.m_index += 1
                messages.append(inMessage)
                inEnum = None
                if "{" in line and line.endswith("}"):
                    inMessage = None
                continue
            if line.startswith("}"):
                inEnum = None
                inMessage = None
                continue
            if inEnum:
                value = self.parseEnumValue(line)
                if value:
                    inEnum["values"].append(value)
                continue
            if not inMessage:
                continue
            field = self.parseField(line)
            if not field:
                continue
            key, keyType, no, isRepeated = field
            inMessage["fields"].append({
                "name": key,
                "type": keyType,
                "no": no,
                "isRepeated": isRepeated,
            })
        return { "header": header, "enums": enums, "messages": messages }

    def parseEnumValue(self, line):
        match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(-?\d+)\s*$', line)
        if not match:
            return None
        return { "name": match.group(1), "no": int(match.group(2)) }

    def toProtoData(self, doc):
        protoData = {}
        for msg in doc["messages"]:
            protoData[msg["name"]] = { "ProtoIdx": msg["protoIdx"] }
            for field in msg["fields"]:
                protoData[msg["name"]][field["name"]] = {
                    "type": field["type"],
                    "no": field["no"],
                    "isRepeated": field["isRepeated"],
                }
        return protoData

    def parseField(self, line):
        isRepeated = False
        if line.startswith("repeated "):
            isRepeated = True
            line = line[len("repeated "):].strip()
        elif line.startswith("optional "):
            line = line[len("optional "):].strip()
        elif line.startswith("required "):
            line = line[len("required "):].strip()
        mapMatch = re.match(r'^(map<[^>]+>)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+)\s*$', line)
        if mapMatch:
            keyType = re.sub(r'\s+', '', mapMatch.group(1))
            return mapMatch.group(2), keyType, int(mapMatch.group(3)), False
        match = re.match(r'^(.+?)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\d+)\s*$', line)
        if not match:
            return None
        return match.group(2), match.group(1).strip(), int(match.group(3)), isRepeated

    def getProtos(self):
        return self.m_protos

    def getProto(self, fileName, key):
        protoData = self.m_protos.get(fileName, {})
        return protoData.get(key, {})

    def onNewFile(self, filePath):
        context = self.m_protoWriter.createEmptyFile(filePath)
        self.parser(filePath, context)

    def onDeleteFile(self, filePath):
        fileName = getFileNameInPath(filePath)
        if not fileName:
            return
        self.m_protos.pop(fileName, None)
        self.m_protoWriter.close(fileName)

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
