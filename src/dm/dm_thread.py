import threading
import time

from pydmsoft import DM
from os import path
from src import teams,util
from src.core import config, game
from src.dm.dm_util import DmUtil


class DmThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.dm = DM()
        self.__running = threading.Event()
        self.__running.set()
        self.__flag = threading.Event()
        self.__flag.set()
        self.reg()
        self.dm_util = DmUtil(self.dm)

    def run(self):
        print(self.getName() + "线程启动")
        while self.is_running():
            game_thread = 0
            user = teams.get_user()
            if teams.login_steam2(self, user):
                hwnd = game.get_hwnd()  # 进入游戏到主界面
                game_thread = GameThread(user, hwnd)
                game_thread.setName('GameThread')
                game_thread.setDaemon(True)
                game_thread.start()
                # 启动守护线程 用于关闭干扰界面
                t_close = CloseThread(hwnd)
                t_close.setDaemon(True)
                t_close.setName('CloseThread')
                t_close.start()
            if game_thread != 0:
                game_thread.join(int(config.get("启动参数", "等待时间")))
                util.stop_thread_name('CloseThread')
                util.stop_thread_name('GameThread')
            time.sleep(5)

    def is_running(self):
        self.__flag.wait()
        return self.__running.isSet()

    def pause(self):
        print(self.getName() + "线程暂停")
        self.__flag.clear()

    def resume(self):
        print(self.getName() + "线程回复")
        self.__flag.set()

    def stop(self):
        print(self.getName() + "线程停止")
        self.__running.clear()

    def reg(self):
        self.dm.SetShowErrorMsg(0)
        print(path.abspath(path.join(path.dirname(__file__), 'resource/')))
        self.dm.SetPath(path.abspath(path.join(path.dirname(__file__), 'resource/')))
        self.dm.SetDict(0, 'dic.txt')
        self.dm.UseDict(0)
        self.dm.LoadPic('*.bmp')
        print(f'是否开启平滑{self.dm.CheckFontSmooth()}')
        print(f'系统色深度{self.dm.GetScreenDepth()}')
        print(f'系统宽高{self.dm.GetScreenWidth()}:{self.dm.GetScreenHeight()}')


class GameThread(threading.Thread):
    def __init__(self, user, hwnd):
        super().__init__()
        self.user = user
        self.hwnd = hwnd

    def run(self):
        print('game')
        task = config.get("启动参数", "任务选项")
        for map_key in task.split(","):
            game.FUNCTION_MAP.get(map_key)()
        teams.task_done(self.user, self.user[0] != 0)  # 添加完成标志


class CloseThread(threading.Thread):
    def __init__(self, hwnd):
        super().__init__()
        self.hwnd = hwnd

    def run(self):
        print('close')
