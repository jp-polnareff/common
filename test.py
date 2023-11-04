import time

from src import const

import win32gui

from src.core import game
from src.dm.dm_regist import dm
from src.dm.dm_util import DmUtil

dm_util = DmUtil(dm)


def get_window_info(hwnd, lParam):
    class_name = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    print(f"句柄：{hwnd} Class Name: {class_name}, Title: {title}")


# 获取所有窗口并遍历它们
win32gui.EnumWindows(get_window_info, None)

print(dm_util.existStr(*const.steam_retry))
print(dm_util.existStr(*const.steam_retry_connect))

# hwnd = dm_util.findWindow('SDL_app', 'Steam')
# dm.MoveWindow(hwnd, 0, 0)
# dm.SetWindowSize(hwnd, 1010, 600)
# dm.SetWindowState(hwnd, 8)
# hwnd = dm_util.findWindow("DOAX VenusVacation", "DOAX VenusVacation")
# hwnd = dm_util.findWindow("DOAX VenusVacation", "DOAX VenusVacation Launcher")
# print(dm.BindWindow(hwnd, 'normal', 'windows', 'windows', 0))


print('结束')
time.sleep(100)
