# -*- coding: utf-8 -*-
import ctypes
import os
from os import path

import win32api
import win32com.client
import win32con
from pymem.ressources.kernel32 import WriteProcessMemory

dm_path = path.abspath(path.join(path.dirname(__file__), 'dm.dll'))
p = os.getcwd()
print(r'regsvr32 /s %s' % dm_path)
print(os.system(r'regsvr32 /s %s' % dm_path))
dm = win32com.client.Dispatch('dm.dmsoft')
print(dm.Ver())
pid = win32api.GetCurrentProcessId()
mydll = win32api.GetModuleHandle("dm.dll")
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
newdata = ctypes.c_long(1)
if WriteProcessMemory(int(handle), mydll + 0x109590, ctypes.byref(newdata), 1, None):
    print('成功改写内存!')
else:
    print('写内存错误!')
