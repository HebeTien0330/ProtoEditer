'''
:@Author: tangchengqin
:@Date: 2025/1/18 14:34:31
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 15:58:27
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.parser import getParser
import importlib.util
import sys
import os

class Exporter:

    def __init__(self, data):
        self.m_data = data
        self.m_protos = {}

    def getProtosData(self, target):
        parser = getParser()
        parser.reset()
        for entry in os.listdir(target):
            fullPath = os.path.join(target, entry)
            if os.path.isdir(fullPath):
                continue
            with open(fullPath, "r", encoding="utf-8") as file:
                context = file.read()
                try:
                    res = parser.parser(entry, context)
                    self.m_protos[entry] = res
                except:
                    continue
        return self.m_protos

    def run(self):
        exportTarget = self.m_data.get("exportTarget")
        if not exportTarget or not os.path.isdir(exportTarget):
            return
        exportPath = self.m_data.get("exportPath")
        if not exportPath or not os.path.isdir(exportPath):
            return
        exportScript = self.m_data.get("exportScript")
        if not exportScript or not os.path.isfile(exportScript):
            return
        protosData = self.getProtosData(exportTarget)
        spec = importlib.util.spec_from_file_location("customScript", exportScript)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        CustomScript = module.CustomScript
        CustomScript(exportPath).run(protosData)
