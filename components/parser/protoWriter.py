'''
:@Author: tangchengqin
:@Date: 2025/1/16 14:48:41
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 17:25:59
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.event import installEventSystem
from components.utils import getFileNameInPath, swapDictKeys

class ProtoWriter:

    def __init__(self):
        self.m_protos = {}
        self.m_update = {}
        self.m_originPath = {}
        installEventSystem(self)
        self.listen("onSave", self.write)

    def open(self, path, protoData):
        fileName = getFileNameInPath(path)
        self.m_protos[fileName] = protoData
        self.m_update[fileName] = False
        self.m_originPath[fileName] = path

    def add(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        protoName = delta.get("proto")
        proto = protos.get(protoName)
        if not proto:
            return
        fieldType = delta.get("type")
        fieldName = delta.get("field")
        isRepeated = delta.get("repeated", False)
        if not fieldType or not fieldName:
            return
        no = len(proto)
        proto[fieldName] = {
            "type": fieldType,
            "no": no,
            "isRepeated": isRepeated
        }
        self.m_protos[fileName][protoName] = proto
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def addRoot(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        protoName = delta.get("proto")
        if not protoName:
            return
        protoIdx = delta.get("ProtoIdx")
        if not protoIdx:
            return
        self.m_protos[fileName][protoName] = {
            "ProtoIdx": protoIdx
        }
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def edit(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        protoName = delta.get("proto")
        proto = protos.get(protoName)
        if not proto:
            return
        fieldType = delta.get("type")
        fieldName = delta.get("field")
        fieldNo = delta.get("no")
        isRepeated = delta.get("repeated", False)
        oldField = delta.get("oldField")
        if not fieldType or not fieldName or not fieldNo or not oldField:
            return
        del proto[oldField]
        proto[fieldName] = {
            "type": fieldType,
            "no": fieldNo,
            "isRepeated": isRepeated
        }
        self.m_protos[fileName][protoName] = proto
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def delete(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        protoName = delta.get("proto")
        proto = protos.get(protoName)
        if not proto:
            return
        targetField = delta.get("field")
        if targetField not in proto:
            return
        fieldNo = proto[targetField]["no"]
        del proto[targetField]
        for field, info in proto.items():
            if not isinstance(info, dict):
                continue
            if info["no"] <= fieldNo:
                continue
            info["no"] -= 1
        self.m_protos[fileName][protoName] = proto
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def deleteRoot(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        protoName = delta.get("proto")
        proto = protos.get(protoName)
        if not proto:
            return
        del protos[protoName]
        self.m_protos[fileName] = protos
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def swap(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        proto = delta.get("proto")
        info = protos.get(proto)
        if not info:
            return
        curField, targetField = delta.get("curField"), delta.get("targetField")
        if not info.get(curField) or not info.get(targetField):
            return
        info[curField]["no"], info[targetField]["no"] = info[targetField]["no"], info[curField]["no"]
        # 排序
        def sortKey(item):
            _, value = item
            if isinstance(value, dict):
                return (1, value['no'])
            return (0, 0)
        info = dict(sorted(info.items(), key=sortKey))
        self.m_protos[fileName][proto] = info
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def swapRoot(self, delta):
        fileName = delta.get("fileName")
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        proto = delta.get("proto")
        protoNames = list(protos.keys())
        index = protoNames.index(proto)
        direction = delta.get("direction")
        if direction == "up":
            if index <= 0:
                return
            targetProto = protoNames[index - 1]
            protos = swapDictKeys(protos, proto, targetProto)
        elif direction == "down":
            if index >= len(protos) - 1:
                return
            targetProto = protoNames[index + 1]
            protos = swapDictKeys(protos, proto, targetProto)
        else:
            return
        self.m_protos[fileName] = protos
        self.m_update[fileName] = True
        self.write()
        return self.m_protos[fileName]

    def write(self):
        for fileName, dirty in self.m_update.items():
            if not dirty:
                continue
            self.doWrite(fileName)
    def doWrite(self, fileName):
        protos = self.m_protos.get(fileName)
        if not protos:
            return
        context = """syntax = "proto3";

package protocol.room;

option go_package = "/message";
"""
        for protocol, data in protos.items():
            message = ""
            for param, info in data.items():
                if param == "ProtoIdx":
                    continue
                if info["isRepeated"]:
                    message += f"""
  repeated {info["type"]} {param} = {info["no"]};"""
                    continue
                message +=f"""
  {info["type"]} {param} = {info["no"]};"""
                
            message = """
message %s {%s
}
""" % (protocol, message)

            context += message

        # print(context)
        with open(self.m_originPath[fileName], "w") as f:
            f.write(context)

    def createEmptyFile(self, filePath):
        context = """syntax = "proto3";

package protocol.room;

option go_package = "/message";
"""
        with open(filePath, "w") as f:
            f.write(context)
        return context
