'''
:@Author: tangchengqin
:@Date: 2025/1/18 14:22:43
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 16:15:31
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
    Gen proto file for python
    """
    def __init__(self, targetDir):
        super().__init__(targetDir)
        finalPath =  f"{self.m_targetDir}\\genForPython"
        if not os.path.exists(finalPath):
            os.makedirs(finalPath)
        self.m_targetDir = finalPath

    def createProtoMap(self, protosData):
        self.log("creating proto map...")
        ret = {}
        for _, protos in protosData.items():
            for protocol, data in protos.items():
                if protocol.startswith("S2C"):
                    continue
                prefix = protocol[:3].lower()
                _protocol =  prefix + "_" + "_".join(map(lambda x: x.lower(), splitUppercase(protocol[3:])))
                ret[_protocol] = protocol

        with open(f"{self.m_targetDir}\\protoMap.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(ret, indent=4, ensure_ascii=False))
        self.log("create proto map finish")

    def createProtoFile(self, protosData):
        self.log("creating proto file...")
        protosDir = f"{self.m_targetDir}\\proto"
        if not os.path.exists(protosDir):
            os.makedirs(protosDir)
        self.Aggregate(protosDir, protosData)
        for filename, protos in protosData.items():
            context = """
syntax = "proto3";

package protocol.%s;
""" % filename.split(".")[0]
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
            with open(f"{protosDir}/{filename}", "w", encoding="utf-8") as file:
                file.write(context)
        self.log("create proto finish...")

    def Aggregate(self, protosDir, protosData):
        context = """
syntax = "proto3";

package protocol;

"""

        payload = ""

        with open(f"{protosDir}/message.proto", "w", encoding="utf-8") as file:
            for filename, protos in protosData.items():
                context += f'import "{filename}";\n'
                filename = filename.split(".")[0]
                for protocol, data in protos.items():
                    prefix = protocol[:3].lower()
                    _protocol =  prefix + "_" + "_".join(map(lambda x: x.lower(), splitUppercase(protocol[3:])))
                    payload += f'\t\tprotocol.{filename}.{protocol} {_protocol} = {data["ProtoIdx"]};\n'

            context += """

message MessageWrapper {
    oneof payload {
%s
    }
}
""" % payload
            file.write(context)

    def genCode(self):
        self.log("start creating code...")
        curOs = checkOS()
        codeDir = f"{self.m_targetDir}\\code"
        if not os.path.exists(codeDir):
            os.mkdir(codeDir)
        protoDir = f"{self.m_targetDir}\\proto"
        if curOs == "Windows":
            command = f"{os.getcwd()}\\tools\\protoc.exe --python_out={codeDir} --proto_path={protoDir} {protoDir}\\*.proto"
            subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
            return
        if curOs == "Linux":
            command = f"{os.getcwd()}/tools/protoc --python_out={codeDir} --proto_path={protoDir} {protoDir}/*.proto"
            subprocess.run([command], capture_output=True, text=True)
        self.log("create code finish...")

    def run(self, protosData):
        self.log("start gen proto file for python...")
        self.createProtoMap(protosData)
        self.createProtoFile(protosData)
        self.genCode()
        self.log("finish all task!")
