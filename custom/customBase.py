'''
:@Author: tangchengqin
:@Date: 2025/1/17 16:55:50
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 14:57:27
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from components.event import installEventSystem
import datetime

class CustomBase:

    def __init__(self, targetDir):
        self.m_targetDir = targetDir
        installEventSystem(self)

    def createProtoFile(self, protosData):
        raise NotImplementedError

    def log(self, text):
        logout = f"[{datetime.datetime.now()}]: {text}\n"
        self.onEvent("onAppendExportInfo", None, logout)
