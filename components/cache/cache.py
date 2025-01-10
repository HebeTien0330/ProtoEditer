'''
:@Author: tangchengqin
:@Date: 2025/1/10 16:41:49
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/10 16:41:49
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
from logger import logfile
import pickle
import os

class Cache:

    def __init__(self):
        self.m_data = {}
        self.m_dirty = 0        # 脏标记

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        self.__dict__["m_dirty"] = 1

    def load(self):
        logfile("cache", "load cache start!")
        if not os.path.exists("cache.pkl"):
            logfile("cache", "cache.pkl does not exist!")
            return
        with open("cache.pkl", "rb") as pickleFile:
            loadedCache = pickle.load(pickleFile)
            if isinstance(loadedCache, Cache):
                self.m_data = loadedCache.m_data
                self.m_dirty = 0
            else:
                logfile("cache", "error load cache, data broken!")
        logfile("cache", "load cache end!")

    def save(self):
        if not self.m_dirty:
            return
        logfile("cache", "save cache start!")
        with open("cache.pkl", "wb") as pickleFile:
            pickle.dump(self, pickleFile)
            self.m_dirty = 0
        logfile("cache", "save cache end!")

    def update(self, key, value):
        self.m_data[key] = value
        self.m_dirty = 1

    def query(self, key):
        return self.m_data.get(key)


if "g_cache" not in globals():
    global g_cache
    g_cache = Cache()

def getCache():
    if "g_cache" not in globals():
        global g_cache
        g_cache = Cache()
    return g_cache

def save():
    cache = getCache()
    if not cache:
        return
    cache.save()

def update(key, value):
    cache = getCache()
    if not cache:
        return
    cache.update(key, value)

def query(key):
    cache = getCache()
    if not cache:
        return
    return cache.query(key)
