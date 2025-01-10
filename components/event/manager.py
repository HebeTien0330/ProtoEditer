'''
:@Author: tangchengqin
:@Date: 2024/9/24 10:08:32
:@LastEditors: tangchengqin
:@LastEditTime: 2024/9/24 10:08:32
:Description: 
:Copyright: Copyright (©)}) 2024 Clarify. All rights reserved.
'''

from .event import Event

class EventManager:

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = EventManager()
        return cls._instance
    
    def __init__(self, EventName, Callback, Filter=None):
        self.m_EventMap = {}
        self.m_OnceEventMap = {}
        self.m_Counter = 1

    def Listen(self, EventName, Callback, Filter=None):
        CallbackList = self.m_EventMap.get(EventName, [])
        EvtId = self.m_Counter
        CallbackList.append(Event(EvtId, EventName, Callback, Filter))
        self.m_Counter += 1
        return EvtId
    
    def ListenOnce(self, EventName, Callback, Filter=None):
        CallbackList = self.m_OnceEventMap.get(EventName, [])
        EvtId = self.m_Counter
        CallbackList.append(Event(EvtId, EventName, Callback, Filter))
        self.m_Counter += 1
        return EvtId
    
    def On(self, EventName, Callback, Filter=None, Once=False):
        if Once:
            return self.ListenOnce(EventName, Callback, Filter)
        return self.Listen(EventName, Callback, Filter)
    
    def Cancel(self, EventName, EvtId):
        EventList = self.m_EventMap.get(EventName)
        if not EventList:
            return False
        for idx, Event in enumerate(EventList):
            if Event.GetEvtId() != EvtId:
                continue
            EventList.pop(idx)
            break
        return True
    
    def CancelOnce(self, EventName, EvtId):
        EventList = self.m_OnceEventMap.get(EventName)
        if not EventList:
            return False
        for idx, Event in enumerate(EventList):
            if Event.GetEvtId() != EvtId:
                continue
            EventList.pop(idx)
            break
        return True

    def CancelAll(self, EventName):
        del self.m_EventMap[EventName]
        del self.m_OnceEventMap[EventName]
        return True

    def Off(self, EventName, EvtId=None, Once=False):
        if not EvtId:
            return self.CancelAll(EventName)
        if Once:
            return self.CancelOnce(EventName, EvtId)
        return self.Cancel(EventName, EvtId)
    
    def Execute(self, EventName, EvtId=None, *args, **kwargs):
        EventList = self.m_EventMap.get(EventName)
        if not EventList:
            return False
        if EvtId:
            for Event in EventList:
                if Event.GetEvtId() != EvtId:
                    continue
                Event.Execute(*args, **kwargs)
                break
            else:
                return False
        else:
            for Event in EventList:
                Event.Execute(*args, **kwargs)
        return True
    
    def ExecuteOnce(self, EventName, EvtId=None, *args, **kwargs):
        EventList = self.m_OnceEventMap.get(EventName)
        if not EventList:
            return False
        if EvtId:
            for idx, Event in enumerate(EventList):
                if Event.GetEvtId() != EvtId:
                    continue
                Event.Execute(*args, **kwargs)
                EventList.pop(idx)
                break
            else:
                return False
        else:
            for idx, Event in enumerate(EventList):
                Event.Execute(*args, **kwargs)
            del self.m_OnceEventMap[EventName]
        return True

    def Call(self, EventName, EvtId=None, *args, **kwargs):
        res1 = self.Execute(EventName, EvtId, *args, **kwargs)
        res2 = self.ExecuteOnce(EventName, EvtId, *args, **kwargs)
        return res1 or res2
    

def Listen(EventName, Callback, Filter=None, Once=False):
    return EventManager().On(EventName, Callback, Filter, Once)

def ListenMulti(EventList):
    Res = []
    for EventName, Callback, Filter, Once in EventList:
        EvtId = Listen(EventName, Callback, Filter, Once)
        Res.append(EvtId)
    return Res

def Cancel(EventName, EvtId=None, Once=False):
    return EventManager().Off(EventName, EvtId, Once)

def OnEvent(EventName, EvtId=None, *args, **kwargs):
    return EventManager().Call(EventName, EvtId, *args, **kwargs)
