import time
import pyautogui as auto
import win32gui
from PIL import Image
import config as cf
import operate

CURRENT = 'teams'  # teams&game


def eat_water(auto_power):
    if auto_power:
        if operate.find_user_water():
            auto.click(1278, 590)
            auto.click(1278, 590)
            auto.click(1278, 590)


def close_interference():
    auto_power = cf.get('全局参数', '自动体力') == '是'
    while True:
        if CURRENT == 'teams':
            close_setup()
        elif CURRENT == 'game':
            close_ok()
            check_get()
            close_notice()
            close_retry()
            click_skip()
            open_auto_fight()
            close_check()
            eat_water(auto_power)
        time.sleep(1)


def close_setup():
    hwnd = win32gui.FindWindow("vguiPopupWindow", "安装 - DEAD OR ALIVE Xtreme Venus Vacation")
    if hwnd != 0:
        win32gui.SetForegroundWindow(hwnd)
        auto.click(1019, 696)


def close_ok():
    im = Image.open("./pic/ok.bmp")
    point = auto.locateCenterOnScreen(im, region=(1213, 658, 135, 57), confidence=0.8)
    if point:
        auto.click(point[0], point[1])


def close_check():
    im = Image.open("./pic/确定.bmp")
    point = auto.locateCenterOnScreen(im, region=(1229, 759, 98, 82), confidence=0.8)
    if point:
        auto.click(point[0], point[1])


def click_skip():
    im = Image.open("./pic/跳过.bmp")
    point = auto.locateCenterOnScreen(im, region=(1700, 860, 120, 50), confidence=0.8)
    if point:
        auto.click(point[0], point[1])
    im = Image.open("./pic/跳过单个.bmp")
    point = auto.locateCenterOnScreen(im, region=(1730, 862, 90, 48), confidence=0.8)
    if point:
        auto.click(point[0], point[1])


def close_notice():
    im = Image.open("./pic/关闭.bmp")
    point = auto.locateCenterOnScreen(im, region=(1830, 215, 63, 54), confidence=0.8)
    if point:
        auto.click(point[0], point[1])


def close_retry():
    im = Image.open("./pic/确认重试.bmp")
    point = auto.locateCenterOnScreen(im, region=(1210, 374, 137, 59), confidence=0.8)
    if point:
        auto.click(1345, 769)


def open_auto_fight():
    im = Image.open("./pic/自动战斗开关.bmp")
    point = auto.locateCenterOnScreen(im, region=(1558, 762, 75, 67), confidence=0.8)
    if point:
        auto.click(point[0], point[1])


def check_get():
    im = Image.open("./pic/确认领取.bmp")
    point = auto.locateCenterOnScreen(im, region=(1200, 379, 145, 52), confidence=0.8)
    if point:
        auto.click(1345, 769)
