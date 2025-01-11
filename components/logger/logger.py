'''
:@Author: tangchengqin
:@Date: 2025/1/10 16:49:11
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 17:37:25
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
        self.m_maxFiles = 10
        self.init()

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def __del__(self):
        for fileHandle in self.m_fileHandles.values():
            fileHandle.close()

    def init(self):
        if os.path.exists(self.m_path):
            return
        os.makedirs(self.m_path)

    def setLogPath(self, path):
        self.m_path = path
        self.init()

    def logfile(self, src, text):
        logout = f"[{datetime.datetime.now()}]: {text}\n"
        if src not in self.m_fileHandles:
            if len(self.m_fileHandles) >= self.m_maxFiles:
                oldest_src = next(iter(self.m_fileHandles))
                oldest_file_handle = self.m_fileHandles.pop(oldest_src)
                oldest_file_handle.close()
            self.m_fileHandles[src] = open(f"{self.m_path}/{src}.log", 'a')
        else:
            self.m_fileHandles[src] = self.m_fileHandles.pop(src)
        
        self.m_fileHandles[src].write(logout)
        self.m_fileHandles[src].flush()
        print(logout, end="")


if "g_Logger" not in globals():
    global g_Logger
    g_Logger = Logger()

def getLogger():
    global g_Logger
    if "g_Logger" not in globals():
        global g_Logger
        g_Logger = Logger()
    return g_Logger

def logfile(src, text):
    logger = getLogger()
    if not logger:
        return
    logger.logfile(src, text)

def setLogPath(path):
    logger = getLogger()
    if not logger:
        return
    logger.setLogPath(path)
    logfile("logger", f"set log path to {path}")
