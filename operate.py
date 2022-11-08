import random
import time

import pyautogui as auto
from PIL import Image


def click_random(x=None, y=None, clicks=1, interval=0.2, duration=0.3, click_r=2,
                 interval_r=random.randint(1, 10) / 20.0, duration_r=random.randint(1, 10) / 20.0):
    auto.moveTo(x, y, duration=duration + duration_r)
    time.sleep(0.1)
    auto.click(x + random.randint(-click_r, click_r), y + random.randint(-click_r, click_r), clicks=clicks,
               interval=interval + interval_r, duration=0.1)


def find_game_ico():
    im = Image.open("./pic/游戏启动.bmp")
    return auto.locateCenterOnScreen(im, region=(8, 215, 127, 811), confidence=0.8)


def find_start_game():
    im = Image.open("./pic/开始游戏.bmp")
    return auto.locateCenterOnScreen(im, region=(1673, 446, 1847, 513), confidence=0.8)


def find_start_panel():
    im = Image.open("./pic/选项.bmp")
    return auto.locateCenterOnScreen(im, region=(732, 210, 817, 261), confidence=0.8)


def find_home_page():
    im = Image.open("./pic/主页.bmp")
    return auto.locateCenterOnScreen(im, region=(658, 245, 763, 338), confidence=0.8)


def find_challenge_return():
    im = Image.open("./pic/挑战赛_返回.bmp")
    return auto.locateCenterOnScreen(im, region=(1431, 825, 55, 62), confidence=0.8)


def return_home_page():
    """
    返回主页
    """
    while find_home_page() is None:
        if find_user_water():
            click_random(1202, 787)
        point = find_challenge_return()
        if point:
            click_random(point[0], point[1])
        time.sleep(1)
        click_random(695, 283)
        move_common()


def find_egg_detail():
    im = Image.open("./pic/扭蛋详情.bmp")
    return auto.locateCenterOnScreen(im, region=(1760, 298, 1852, 380), confidence=0.8)


def click_home_egg():
    im = Image.open("./pic/主页_扭蛋.bmp")
    point = auto.locateCenterOnScreen(im, region=(637, 561, 814, 689), confidence=0.80)
    if point:
        click_random(point[0], point[1], click_r=0)
        auto.moveTo(1530, 471, duration=0.5)


def find_check_egg():
    im = Image.open("./pic/确认扭蛋.bmp")
    return auto.locateCenterOnScreen(im, region=(1219, 382, 1330, 421), confidence=0.8)


def find_not_get_egg():
    im = Image.open("./pic/无法抽扭蛋.bmp")
    return auto.locateCenterOnScreen(im, region=(1198, 380, 1335, 426), confidence=0.8)


def find_egg_result():
    im = Image.open("./pic/扭蛋结果.bmp")
    return auto.locateCenterOnScreen(im, region=(1563, 224, 1698, 308), confidence=0.80)


def find_use_count():
    im = Image.open("./pic/使用次数.bmp")
    return auto.locateCenterOnScreen(im, region=(1167, 376, 1379, 424), confidence=0.8)


def move_common():
    auto.moveTo(819, 212, duration=0.5)


def click_common():
    click_random(819, 212, duration=0.2)


def find_game_cancel():
    im = Image.open("./pic/挑战赛_取消.bmp")
    return auto.locateCenterOnScreen(im, region=(1167, 376, 1379, 424), confidence=0.8)


def enter_game():
    """
    进入挑战赛
    """
    im2 = Image.open("./pic/挑战赛_活动.bmp")
    while not auto.locateCenterOnScreen(im2, region=(1816, 304, 1893, 469), confidence=0.8):
        click_random(692, 375)
        im = Image.open("./pic/主页_挑战赛.bmp")
        while auto.locateCenterOnScreen(im, region=(660, 380, 747, 419), confidence=0.8):
            point = auto.locateCenterOnScreen(im, region=(660, 380, 747, 419), confidence=0.8)
            if point:
                auto.click(point[0], point[1], duration=0.5)
                move_common()
            time.sleep(2)


def click_game_active():
    im2 = Image.open("./pic/挑战赛_活动.bmp")
    time.sleep(3)
    point = auto.locateCenterOnScreen(im2, region=(1816, 304, 1893, 469), confidence=0.8)
    if point:
        click_random(point[0], point[1])
    while not find_challenge_type("活动"):
        click_random(692, 375)
        point = auto.locateCenterOnScreen(im2, region=(1816, 304, 1893, 469), confidence=0.8)
        if point:
            click_random(point[0], point[1])
        time.sleep(2)


def find_game_active_gold():
    im = Image.open("./pic/挑战赛_活动_金色.bmp")
    return auto.locateCenterOnScreen(im, region=(1775, 510, 52, 36), confidence=0.90)


def game_active_while():
    """
    活动循环挑战new
    """
    while not find_game_cancel():
        if not find_game_active_gold():
            click_random(1733, 553)
        elif not find_game_active_100(2):
            click_random(1763, 625)
        else:
            click_random(1733, 553)
        move_common()
    im = Image.open("./pic/挑战赛_活动_s.bmp")
    while not auto.locateCenterOnScreen(im, region=(1836, 521, 64, 61), confidence=0.8):
        point = find_game_challenge()
        while not point:
            click_random(1743, 554)
            time.sleep(2)
            point = find_game_challenge()
        while point:
            click_random(point[0], point[1])
            time.sleep(5)
            point = find_game_challenge()
            if find_user_water():
                return False
        if find_user_water():
            return False
        time.sleep(6)
        while not find_game_cancel():
            time.sleep(0.5)
            click_common()
    return True


def find_user_water():
    im = Image.open("./pic/恢复饮料.bmp")
    return auto.locateCenterOnScreen(im, region=(1219, 372, 139, 56), confidence=0.8)


def find_game_active_100(index=1):
    im = Image.open("./pic/挑战赛_活动_100.bmp")
    if index == 1:
        return auto.locateCenterOnScreen(im, region=(1813, 540, 58, 29), confidence=0.90)
    elif index == 2:
        return auto.locateCenterOnScreen(im, region=(1807, 610, 62, 34), confidence=0.90)


def find_check():
    im = Image.open("./pic/签到.bmp")
    return auto.locateCenterOnScreen(im, region=(1576, 263, 305, 238), confidence=0.8)


def find_check_inner():
    im = Image.open("./pic/签到_内.bmp")
    return auto.locateCenterOnScreen(im, region=(934, 340, 749, 446), confidence=0.8)


def receive_check():
    return_home_page()
    while find_check():
        point = find_check()
        if point:
            click_random(point[0], point[1])
            move_common()
            time.sleep(1)
    time.sleep(5)
    point1 = find_check_inner()
    if point1:
        click_random(point1[0], point1[1])
        return True
    return False


def find_mail():
    im = Image.open("./pic/信箱.bmp")
    return auto.locateCenterOnScreen(im, region=(638, 812, 88, 85), confidence=0.8)


def find_mail_get():
    im = Image.open("./pic/信箱_全部领取.bmp")
    return auto.locateCenterOnScreen(im, region=(1367, 794, 183, 69), confidence=0.80)


def find_none_item():
    im = Image.open("./pic/信箱_没有道具.bmp")
    return auto.locateCenterOnScreen(im, region=(1201, 531, 113, 43), confidence=0.80)


def receive_mail():
    return_home_page()
    while find_mail():
        point = find_mail()
        if point:
            click_random(point[0], point[1])
            move_common()
            time.sleep(1)
    time.sleep(5)
    while auto.pixelMatchesColor(1142, 302, (247, 77, 99)):
        click_random(1142, 302)
        click_random(1457, 830)
        time.sleep(10)
    while auto.pixelMatchesColor(1340, 302, (247, 77, 99)):
        click_random(1340, 302)
        click_random(1457, 830)
        time.sleep(10)


def find_task():
    im = Image.open("./pic/任务.bmp")
    return auto.locateCenterOnScreen(im, region=(851, 797, 91, 96), confidence=0.80)


def receive_task():
    return_home_page()
    while find_task():
        point = find_task()
        if point:
            click_random(point[0], point[1])
            move_common()
            time.sleep(1)
    time.sleep(10)
    while auto.pixelMatchesColor(1081, 328, (247, 77, 99)):
        click_random(1045, 346)
        click_random(1507, 821)
        time.sleep(10)

    while auto.pixelMatchesColor(1234, 328, (247, 77, 99)):
        click_random(1197, 340)
        click_random(1507, 821)
        time.sleep(10)

    while auto.pixelMatchesColor(1387, 328, (247, 77, 99)):
        click_random(1351, 344)
        click_random(1507, 821)
        time.sleep(10)

    while auto.pixelMatchesColor(1540, 328, (247, 77, 99)):
        click_random(1496, 347)
        click_random(1507, 821)
        time.sleep(10)


def find_game_challenge():
    im2 = Image.open("./pic/挑战赛_挑战.bmp")
    return auto.locateCenterOnScreen(im2, region=(1613, 830, 1728, 901), confidence=0.8)


def find_challenge_type(challenge_type):
    im = Image.open("./pic/挑战赛_看板_" + challenge_type + ".bmp")
    return auto.locateCenterOnScreen(im, region=(822, 226, 170, 120), confidence=0.80)


def click_challenge_type(challenge_type):
    while not find_challenge_type(challenge_type):
        im = Image.open("./pic/挑战赛_" + challenge_type + ".bmp")
        point = auto.locateCenterOnScreen(im, region=(1500, 304, 405, 359), confidence=0.80)
        if point:
            click_random(point[0], point[1])
            time.sleep(3)
