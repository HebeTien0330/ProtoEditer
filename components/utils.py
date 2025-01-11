'''
:@Author: tangchengqin
:@Date: 2025/1/10 18:13:46
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/11 15:54:32
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''

class Functor:

    def __init__(self, func, *args, **kwargs):
        self.m_func = func
        self.m_args = args
        self.m_kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newArgs = tuple(list(self.m_args) + list(args))
        newKwargs = dict(list(self.m_kwargs.items()) + list(kwargs.items()))
        return self.m_func(*newArgs, **newKwargs)

def getFileNameInPath(path):
    return path.split('/')[-1]
