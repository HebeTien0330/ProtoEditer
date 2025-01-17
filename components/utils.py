'''
:@Author: tangchengqin
:@Date: 2025/1/10 18:13:46
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/17 17:44:32
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
import os

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
    return os.path.basename(path)

def swapDictKeys(target, key1, key2):
    keys = list(target.keys())
    # 找到元素的索引
    index1 = keys.index(key1)
    index2 = keys.index(key2)
    keys[index1], keys[index2] = keys[index2], keys[index1]
    return {key: target[key] for key in keys}
