'''
:@Author: tangchengqin
:@Date: 2025/1/10 16:49:11
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/10 17:10:10
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

import os
import datetime

class Logger:

    __isinstance = None

    def __init__(self):
        self.m_fileHandles = {}
        self.m_path = "../log/"
        self.init()

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def __del__(self):
        for file_handle in self.file_handles.values():
            file_handle.close()

    def init(self):
        print(self.m_path, os.path.exists(self.m_path))
        if os.path.exists(self.m_path):
            return
        os.makedirs(self.m_path)

    def setLogPath(self, path):
        self.m_path = path
        self.init()

    def logfile(self, src, text):
        logout = f"[{datetime.datetime.now()}]: {text}\n"
        if src not in self.m_fileHandles:
            if len(self.m_fileHandles) >= self.max_files:
                oldest_src = next(iter(self.m_fileHandles))
                oldest_file_handle = self.m_fileHandles.pop(oldest_src)
                oldest_file_handle.close()
            self.m_fileHandles[src] = open(f"{self.m_path}/{src}.log", 'a')
        else:
            self.m_fileHandles[src] = self.m_fileHandles.pop(src)
        
        self.m_fileHandles[src].write(logout)
        print(logout, end="")


if "g_Logger" not in globals():
    global g_Logger
    g_Logger = Logger()

def getLogger():
    if "g_Logger" not in globals():
        return Logger()
    return g_Logger

def logfile(src, text):
    logger = getLogger()
    if not logger:
        return
    logger.logfile(src, text)
