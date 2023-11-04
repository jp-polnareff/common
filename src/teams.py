import os
import time

from src import const
from src.core import config, game
from src.dm.dm_regist import dm
from src.dm.dm_util import DmUtil
from src.dm.dm_thread import DmThread

dm_util = DmUtil(dm)
account_path = os.path.expanduser("~/Desktop/账号.txt")
team_time_out = 120


def get_user_info():
    with open(account_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()  # 去掉每行头尾空白
            if not line.endswith("已完成"):
                return line.split("----")


def exit_teams():
    os.system('taskkill /f /t /im ' + "steam.exe")
    time.sleep(2)


def task_done(user, done_flag):
    if done_flag:
        str_new = ""
        with open(account_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip().replace('\n', '')  # 去掉每行头尾空白
                if line.split("----")[0] == user[0]:
                    str_new += line + "----已完成" + '\n'
                    continue
                str_new += line + '\n'
        with open(account_path, "w", encoding="utf-8") as f:
            f.write(str_new)


def init_account():
    str_new = ""
    with open(account_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace('----已完成', '')  # 去掉每行头尾空白
            str_new += line + '\n'
    with open(account_path, "w", encoding="utf-8") as f:
        f.write(str_new)
    return None


def login_steam2(self: DmThread, user):
    dm_util = self.dm_util
    dm = self.dm
    if user[0] == 0:
        return True
    dm.RunApp('C:/Program Files (x86)/Steam/steam.exe', 0)
    time.sleep(4)
    start = time.time()
    while self.is_running and in_time(start) and dm_util.findWindowSure('SDL_app', '登录 Steam') == 0 \
            and not dm_util.existPic(*const.denglu):
        dm.RunApp('C:/Program Files (x86)/Steam/steam.exe', 0)
    time.sleep(4)
    hwnd = dm_util.findWindowSure('SDL_app', '登录 Steam')
    dm.SetWindowState(hwnd, 1)
    dm.MoveWindow(hwnd, 607, 320)
    while self.is_running() and in_time(start) and dm_util.existPic(*const.denglu):
        hwnd = dm_util.findWindowSure('SDL_app', '登录 Steam')
        dm.SetWindowState(hwnd, 1)
        dm.MoveWindow(hwnd, 607, 320)
        dm_util.moveToAndLeftDoubleClick(761, 462)
        time.sleep(1)
        print(f'发送用户名{dm.SendString(hwnd, user[0])}')
        time.sleep(1)
        dm_util.moveToAndLeftDoubleClick(766, 531)
        time.sleep(1)
        print(f'发送密码{dm.SendString(hwnd, user[1])}')
        dm_util.findPicLeftClick(*const.jizhuwo)
        time.sleep(1)
        dm_util.findPicLeftClick(*const.denglu)

    while self.is_running() and in_time(start) and dm_util.findWindowSure('SDL_app', 'Steam') == 0:
        if dm_util.existPic(*const.chongshi):
            return False
        print('等待steam登录')
        time.sleep(1)
    hwnd = dm_util.findWindowSure('SDL_app', 'Steam')
    dm_util.setWindowPos(hwnd, 0, 0, 1010, 600, 8)
    if dm_util.existStr(*const.steam_retry):
        print("steam登录重试过多")
        return False
    if dm_util.existStr(*const.steam_retry_connect):
        print("steam连接问题")
        return False
    print('steam登录成功')
    while self.is_running() and in_time(start) and dm_util.findWindowSure("DOAX VenusVacation",
                                                                          "DOAX VenusVacation Launcher") == 0:
        dm_util.setWindowPos(hwnd, 0, 0, 1010, 600, 8)
        dm_util.findPicLeftClickOffset(*const.ku, x=5, y=5)
        dm_util.moveToAndLeftClick(609, 511)
        dm_util.findPicLeftDoubleClick(*const.youxiico)
    print("游戏登录窗口")
    hwnd = dm_util.findWindowSure("DOAX VenusVacation", "DOAX VenusVacation Launcher")
    while self.is_running() and in_time(start) and dm_util.findWindowSure("DOAX VenusVacation",
                                                                          "DOAX VenusVacation") == 0:
        dm_util.setWindowPos(hwnd, 954, 255, 966, 569, 8)
        dm_util.moveToAndLeftDoubleClick(1792, 406)
        dm.MoveTo(579, 620)
        time.sleep(2)
    time.sleep(4)
    dm_util.setWindowPos(hwnd, 634, 165, 1286, 749, 8)
    print("进入游戏")
    return True


def in_time(start):
    time.sleep(1)
    gap = time.time() - start
    if gap > team_time_out:
        print("steam登录超时")
        return False
    return True


def get_user():
    user = [0, 0]
    if config.get('启动参数', '登录teams') == '是':
        # 关闭游戏teams
        game.exit_game()
        exit_teams()
        user = get_user_info()
        print(f'准备登录{user[0]}----{user[1]}')
    return user
