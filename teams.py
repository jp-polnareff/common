import os
import time

import pyautogui as auto
import pyperclip
import win32con
import win32gui
from PIL import Image

import close
import config as cf
import operate


def get_user_info():
    with open('账号.txt', "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # 去掉每行头尾空白
            if not line.endswith("已完成"):
                return line.split("----")


# 打开teams 获取teams登录窗口句柄
def login_teams(username, password):
    close.CURRENT = 'teams'
    # 打开teams
    hwnd = 0
    while hwnd == 0:
        hwnd = win32gui.FindWindow("vguiPopupWindow", "Steam 登录")
        os.popen(cf.get("启动参数", "teams路径"))
        time.sleep(3)
    win32gui.SetForegroundWindow(hwnd)
    auto.click(1006, 440, clicks=2, interval=0.2, button='left')
    # auto.typewrite(username, interval=0.1)
    send_message(username)
    auto.click(1016, 513, clicks=2, interval=0.2, button='left')
    # auto.typewrite(password, interval=0.1)
    send_message(password)
    point = find_remember_me()
    while point is not None:
        auto.click(point)
        time.sleep(1)
        point = find_remember_me()
    auto.moveTo(844, 600)
    auto.click()
    hwnd = win32gui.FindWindow("vguiPopupWindow", "Steam")
    count = 0
    while hwnd == 0:
        count += 1
        time.sleep(3)
        hwnd = win32gui.FindWindow("vguiPopupWindow", "Steam")
        if count > 40:
            exit_teams()
            return False
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1010, 600, win32con.SWP_SHOWWINDOW)
    return True


def exit_teams():
    time.sleep(2)
    os.system('taskkill /f /t /im ' + "steam.exe")
    time.sleep(2)


def send_message(text):
    pyperclip.copy(text)
    time.sleep(1)
    auto.hotkey('ctrl', 'v')


def find_all():
    im = Image.open("./pic/全部.bmp")
    return auto.locateCenterOnScreen(im, region=(18, 207, 66, 228), confidence=0.9)


def find_remember_me():
    im = Image.open("./pic/记住我.bmp")
    return auto.locateCenterOnScreen(im, region=(632, 523, 684, 580), confidence=0.9)


def click_library():
    im = Image.open("./pic/库.bmp")
    point = auto.locateCenterOnScreen(im, region=(92, 7, 130, 99), confidence=0.8)
    if point:
        operate.click_random(point[0], point[1])


def task_done(user, done_flag):
    if done_flag:
        str_new = ""
        with open('账号.txt', "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().replace('\n', '')  # 去掉每行头尾空白
                if line.split("----")[0] == user[0]:
                    str_new += line + "----已完成" + '\n'
                    continue
                str_new += line + '\n'
        with open('账号.txt', "w", encoding="utf-8") as f:
            f.write(str_new)


def init_account():
    str_new = ""
    with open('账号.txt', "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace('----已完成', '')  # 去掉每行头尾空白
            str_new += line + '\n'
    with open('账号.txt', "w", encoding="utf-8") as f:
        f.write(str_new)
    return None
