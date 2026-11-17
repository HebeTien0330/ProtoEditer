'''
:@Author: tangchengqin
:@Date: 2025/1/10 18:13:46
:@LastEditors: tangchengqin
:@LastEditTime: 2025/1/20 11:17:36
:Description: 
:Copyright: Copyright (©) 2025 Clarify. All rights reserved.
'''
import glob
import os
import re
import subprocess
import sys

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

def checkOS():
    if os.name == 'nt':
        return 'Windows'
    if sys.platform == 'darwin':
        return 'Darwin'
    if os.name == 'posix':
        return 'Linux'
    return 'Unknown'

def getProtocPath():
    protocName = 'protoc'
    if checkOS() == 'Windows':
        protocName = 'protoc.exe'
    return os.path.join(os.getcwd(), 'tools', protocName)

def runCommand(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except OSError as exc:
        if not exc:
            return False, '命令无法执行'
        return False, str(exc)
    if result.returncode == 0:
        return True, (result.stdout or '').strip()
    detail = (result.stderr or result.stdout or '').strip()
    if not detail:
        detail = '命令退出码 %s' % result.returncode
    return False, detail

def compileProtos(outFlag, outDir, protoDir):
    binary = getProtocPath()
    if not os.path.isfile(binary):
        return False, '未找到 protoc：%s' % binary
    protos = sorted(glob.glob(os.path.join(protoDir, '*.proto')))
    if not protos:
        return False, '没有可编译的 .proto 文件'
    command = [binary, '--%s=%s' % (outFlag, outDir), '--proto_path=%s' % protoDir]
    command.extend(protos)
    ok, message = runCommand(command)
    if ok:
        return True, 'protoc 完成'
    if checkOS() != 'Darwin':
        if not message:
            return False, 'protoc 执行失败'
        return False, message
    darwinMsg = '当前 tools/protoc 无法在 macOS 上运行，代码生成已跳过。proto 文件已经写出。请安装对应平台的 protoc，或把可执行文件放到 tools/protoc。'
    if message:
        darwinMsg = darwinMsg + '\n' + message
    return False, darwinMsg

def splitUppercase(s):
    # 使用正则表达式找到所有大写字母及其前面的部分
    parts = re.findall('[A-Z][^A-Z]*', s)
    return parts
