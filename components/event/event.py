'''
:@Author: tangchengqin
:@Date: 2024/9/24 10:05:11
:@LastEditors: tangchengqin
:@LastEditTime: 2024/9/24 10:05:11
:Description: 
:Copyright: Copyright (©)}) 2024 Clarify. All rights reserved.
'''

class Event:

    def __init__(self, EvtId, EventName, Callback, Filter=None):
        self.m_EvtId = EvtId
        self.m_EventName = EventName
        self.m_Callback = Callback
        self.m_Filter = Filter

    def GetEvtId(self):
        return self.m_EvtId

    def Execute(self, *args, **kwargs):
        if self.m_Filter and self.m_Filter(*args, **kwargs):
            return
        self.m_Callback(*args, **kwargs)
