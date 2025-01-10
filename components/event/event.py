'''
:@Author: tangchengqin
:@Date: 2024/9/24 10:05:11
:@LastEditors: tangchengqin
:@LastEditTime: 2024/9/24 10:05:11
:Description: 
:Copyright: Copyright (©)}) 2024 Clarify. All rights reserved.
'''

class Event:

    def __init__(self, evtId, eventName, callback, filter=None):
        self.m_evtId = evtId
        self.m_eventName = eventName
        self.m_callback = callback
        self.m_filter = filter

    def getEvtId(self):
        return self.m_evtId

    def execute(self, *args, **kwargs):
        if self.m_filter and self.m_filter(*args, **kwargs):
            return
        self.m_callback(*args, **kwargs)
