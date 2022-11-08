import configparser
import os
import time

import pyautogui as auto
import win32con
import win32gui

import close
import config as cf
import operate
import teams


def check():
    for i in range(2):
        if operate.receive_check():  # 签到奖励
            break
    operate.return_home_page()


def receive_mail():
    operate.receive_mail()  # 邮件奖励
    operate.return_home_page()


def receive_task():
    operate.receive_task()  # 任务奖励
    operate.return_home_page()


def gashapon():
    operate.return_home_page()
    config = configparser.ConfigParser()
    config.read("./config.ini", encoding='utf-8')
    win_num = int(config.get("扭蛋", "抽奖窗口"))
    model_total = int(config.get("扭蛋", "模式总数"))
    model_num = int(config.get("扭蛋", "模式选项"))
    count = int(config.get("扭蛋", "抽奖次数"))
    while operate.find_egg_detail() is None:
        operate.click_home_egg()
        time.sleep(2)
    reward_point = cf.REWARDS_MAP.get(model_total)[model_num - 1]
    time.sleep(1)
    while win_num > 6:
        auto.click(946, 831)
        time.sleep(0.2)
        win_num = win_num - 1
    win_point = cf.WINDOW_MAP.get(win_num)
    auto.click(win_point[0], win_point[1], clicks=3, interval=0.5, button='left', duration=0.5)
    while count > 0:
        auto.click(reward_point[0], reward_point[1])
        time.sleep(1)
        if operate.find_check_egg():
            auto.click(1349, 778)  # 点击确定
        elif operate.find_not_get_egg():
            auto.click(1200, 774)  # 点击取消
            break
        elif operate.find_use_count():
            if count > 10:
                auto.click(1289, 521)
                count = count - 9
                time.sleep(1)
            else:
                count = count - 1
                while count > 0:
                    auto.click(1240, 524)
                    count = count - 1
            auto.click(1342, 792)  # 点击确定
        else:
            continue
        while operate.find_egg_result() is None:
            operate.click_random(1646, 457)
            time.sleep(2)
        count = count - 1
    operate.return_home_page()


def challenge_active():
    while True:
        operate.return_home_page()
        operate.enter_game()
        operate.click_game_active()
        if operate.find_game_active_100(1):
            break
        if not operate.game_active_while():
            break
    operate.return_home_page()


def start_game():
    point = operate.find_game_ico()
    while point is None:
        time.sleep(2)
        teams.click_library()
        point = operate.find_game_ico()
    hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation Launcher")
    while hwnd == 0:
        auto.click(point, clicks=2, interval=0.2, button='left', duration=0.5)
        time.sleep(2)
        hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation Launcher")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 944, 250, 976, 579, win32con.SWP_SHOWWINDOW)
    time.sleep(5)
    point = operate.find_start_game()
    while point is None:
        time.sleep(2)
        point = operate.find_start_game()
    while point is not None:
        auto.moveTo(point, duration=0.5)
        auto.mouseDown()
        time.sleep(1)
        auto.mouseUp()
        operate.move_common()
        point = operate.find_start_game()
        time.sleep(1)
    hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation")
    while hwnd == 0:
        time.sleep(5)
        hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation")
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 624, 160, 1296, 759, win32con.SWP_SHOWWINDOW)
    close.CURRENT = 'game'

    point = operate.find_start_panel()
    while point is None:
        time.sleep(2)
        point = operate.find_start_panel()
    while point is not None:
        point = operate.find_start_panel()
        auto.click(1282, 836, button='left', duration=0.5)
    operate.return_home_page()
    return hwnd


def exit_game():
    time.sleep(2)
    os.system('taskkill /f /t /im ' + "DOAX_VV.exe")
    time.sleep(2)


def challenge_custom():
    """
    挑战赛自定义窗口
    """
    operate.return_home_page()
    operate.enter_game()
    challenge_type = "推荐"
    challenge_num = cf.get("挑战赛-自定义", "挑战窗口")
    operate.click_challenge_type(challenge_type)
    point = operate.find_game_challenge()
    while True:
        while not point:
            window_point = cf.CHALLENGE_POINT_MAP.get(challenge_num)
            operate.click_random(window_point[0], window_point[1])
            operate.move_common()
            time.sleep(2)
            point = operate.find_game_challenge()
        while point:
            operate.click_random(point[0], point[1])
            operate.move_common()
            time.sleep(4)
            point = operate.find_game_challenge()
            if operate.find_user_water():
                break
        if operate.find_user_water():
            break
        time.sleep(6)
        while not operate.find_challenge_type(challenge_type):
            time.sleep(0.5)
            operate.click_common()
    operate.return_home_page()
