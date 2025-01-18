'''
:@Author: tangchengqin
:@Date: 2025/1/10 16:49:11
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/18 14:18:33
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
import os
import datetime

class Logger:

    __isinstance = None

    def __init__(self):
        self.m_fileHandles = {}
        self.m_path = f"{os.getcwd()}\\log"
        self.m_maxFiles = 10
        self.m_persist = False
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

    def save(self):
        for fileHandle in self.m_fileHandles.values():
            fileHandle.close()
        print("all log files close")

    def setLogPath(self, path):
        self.m_path = path
        self.init()

    def setPersist(self, isPresist):
        self.m_persist = isPresist

    def logfile(self, src, text):
        logout = f"[{datetime.datetime.now()}]: {text}\n"
        if src not in self.m_fileHandles:
            if len(self.m_fileHandles) >= self.m_maxFiles:
                oldest_src = next(iter(self.m_fileHandles))
                oldest_file_handle = self.m_fileHandles.pop(oldest_src)
                oldest_file_handle.close()
            self.m_fileHandles[src] = open(f"{self.m_path}/{src}.log", 'a', encoding="utf-8")
        
        if self.m_persist:
            fileHandler = self.m_fileHandles[src]
            fileHandler.write(logout)
            fileHandler.flush()
            os.fsync(fileHandler.fileno())
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
