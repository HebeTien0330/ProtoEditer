'''
:@Author: tangchengqin
:@Date: 2024/9/24 10:08:32
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/10 17:58:33
:Description: 
:Copyright: Copyright (©)}) 2024 Clarify. All rights reserved.
'''

from .event import Event

class EventManager:

    __isinstance = None

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance
    
    def __init__(self):
        self.m_eventMap = {}
        self.m_onceEventMap = {}
        self.m_counter = 1

    def listen(self, eventName, callback, filter=None):
        callbackList = self.m_eventMap.get(eventName, [])
        evtId = self.m_counter
        callbackList.append(Event(evtId, eventName, callback, filter))
        self.m_eventMap[eventName] = callbackList
        self.m_counter += 1
        return evtId
    
    def listenOnce(self, eventName, callback, filter=None):
        callbackList = self.m_onceEventMap.get(eventName, [])
        evtId = self.m_counter
        callbackList.append(Event(evtId, eventName, callback, filter))
        self.m_onceEventMap[eventName] = callbackList
        self.m_counter += 1
        return evtId
    
    def on(self, eventName, callback, filter=None, once=False):
        if once:
            return self.listenOnce(eventName, callback, filter)
        return self.listen(eventName, callback, filter)
    
    def cancel(self, eventName, evtId):
        eventList = self.m_eventMap.get(eventName)
        if not eventList:
            return False
        for idx, event in enumerate(eventList):
            if event.getEvtId() != evtId:
                continue
            eventList.pop(idx)
            break
        return True
    
    def cancelOnce(self, eventName, evtId):
        eventList = self.m_onceEventMap.get(eventName)
        if not eventList:
            return False
        for idx, event in enumerate(eventList):
            if event.getEvtId() != evtId:
                continue
            eventList.pop(idx)
            break
        return True

    def cancelAll(self, eventName):
        del self.m_eventMap[eventName]
        del self.m_onceEventMap[eventName]
        return True

    def off(self, eventName, evtId=None, once=False):
        if not evtId:
            return self.cancelAll(eventName)
        if once:
            return self.cancelOnce(eventName, evtId)
        return self.cancel(eventName, evtId)
    
    def execute(self, eventName, evtId=None, *args, **kwargs):
        eventList = self.m_eventMap.get(eventName)
        if not eventList:
            return False
        if evtId:
            for event in eventList:
                if event.getEvtId() != evtId:
                    continue
                event.execute(*args, **kwargs)
                break
            else:
                return False
        else:
            for event in eventList:
                event.execute(*args, **kwargs)
        return True
    
    def executeOnce(self, eventName, evtId=None, *args, **kwargs):
        eventList = self.m_onceEventMap.get(eventName)
        if not eventList:
            return False
        if evtId:
            for idx, event in enumerate(eventList):
                if event.getEvtId() != evtId:
                    continue
                event.execute(*args, **kwargs)
                eventList.pop(idx)
                break
            else:
                return False
        else:
            for idx, event in enumerate(eventList):
                event.execute(*args, **kwargs)
            del self.m_onceEventMap[eventName]
        return True

    def call(self, eventName, evtId=None, *args, **kwargs):
        res1 = self.execute(eventName, evtId, *args, **kwargs)
        res2 = self.executeOnce(eventName, evtId, *args, **kwargs)
        return res1 or res2
    

if "g_EvtManager" not in globals():
    global g_EvtManager
    g_EvtManager = EventManager()

def getEvtManager():
    if "g_EvtManager" not in globals():
        global g_EvtManager
        g_EvtManager = EventManager()
    return g_EvtManager

def listen(eventName, callback, filter=None, once=False):
    return getEvtManager().on(eventName, callback, filter, once)

def listenMulti(eventList):
    evtManager = getEvtManager()
    res = []
    for eventName, callback, filter, once in eventList:
        evtId = evtManager.on(eventName, callback, filter, once)
        res.append(evtId)
    return res

def cancel(eventName, evtId=None, once=False):
    return getEvtManager().off(eventName, evtId, once)

def onEvent(eventName, evtId=None, *args, **kwargs):
    return getEvtManager().call(eventName, evtId, *args, **kwargs)

def installEventSystem(target):
    funcList = [listen, listenMulti, cancel, onEvent]
    for func in funcList:
        setattr(target, func.__name__, func)
