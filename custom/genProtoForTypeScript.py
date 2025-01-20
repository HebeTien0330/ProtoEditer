'''
:@Author: tangchengqin
:@Date: 2025/1/18 14:22:43
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 16:15:28
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.utils import splitUppercase, checkOS
from custom.customBase import CustomBase
import os
import json
import subprocess

class CustomScript(CustomBase):
    """
    Gen proto file for typescript
    """
    def __init__(self, targetDir):
        super().__init__(targetDir)
        finalPath =  f"{self.m_targetDir}\\genForTypeScript"
        if not os.path.exists(finalPath):
            os.makedirs(finalPath)
        self.m_targetDir = finalPath

    def createProtoRoute(self, protosData):
        self.log("creating proto route...")
        route = {}
        for _, protos in protosData.items():
            for protocol, data in protos.items():
                idx = data["ProtoIdx"]
                if not protocol.startswith("C2S"):
                    continue
                s2cProtocol = "S2C" + protocol[3:]
                route[protocol] = {
                    "seqt": idx,
                    "seqr": protos[s2cProtocol]["ProtoIdx"],
                    "sType": "c2s" + "_" + "_".join(map(lambda x: x.lower(), splitUppercase(protocol[3:]))),
                    "rType": "s2c" + "_" + "_".join(map(lambda x: x.lower(), splitUppercase(protocol[3:]))),
                }
        with open(f"{self.m_targetDir}\\route.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(route, indent=4, ensure_ascii=False))
        self.log("create proto route finish")


    def createProtoFile(self, protosData):
        self.log("creating proto file...")
        context = f"""syntax = "proto3";

package protocol;
    {self.createMessageWrapper(protosData)}
    """
        for filename, protos in protosData.items():
            context += f"""
// ========================={filename.split(".")[0]}========================="""
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

        with open(f"{self.m_targetDir}/protocol.proto", "w", encoding="utf-8") as file:
            file.write(context)
        self.log("create proto finish...")

    def createMessageWrapper(self, protosData):
        context = ""
        for _, protos in protosData.items():
            for protocol, data in protos.items():
                prefix = protocol[:3].lower()
                _protocol =  prefix + "_" + "_".join(map(lambda x: x.lower(), splitUppercase(protocol[3:])))
                context += f"""
    {protocol} {_protocol} = {data["ProtoIdx"]};"""
        context = """
message MessageWrapper {
  oneof payload {%s
  }
}
    """ % context
        return context

    def genCode(self):
        self.log("start creating code...")
        curOs = checkOS()
        if curOs == "Windows":
            command = f"pbjs {self.m_targetDir}\protocol.proto --ts {self.m_targetDir}\protocol.ts"
            subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
            return
        if curOs == "Linux":
            command = f"pbjs {self.m_targetDir}\protocol.proto --ts {self.m_targetDir}\code\protocol.ts"
            subprocess.run([command], capture_output=True, text=True)
        self.log("create code finish...")

    def run(self, protosData):
        self.log("start gen proto file for typescript...")
        self.createProtoRoute(protosData)
        self.createProtoFile(protosData)
        self.genCode()
        self.log("finish all task!")
