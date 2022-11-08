import multiprocessing
import time
import tkinter
import tkinter.messagebox
import win32con
import win32gui
import threading
import close
import config as cf
import game
import teams


def run_task():
    if cf.run_task:
        cf.run_task = False
        user = teams.get_user_info()
        if len(user) != 2:
            tkinter.messagebox.showinfo('提示', '没有需要执行的账号')
        # 任务线程
        process_task = multiprocessing.Process(target=thread_task, name="Process-task", daemon=True)
        process_task.start()
        cf.TEST_TASK_PID = process_task.pid
        # t_task = threading.Thread(target=thread_task, name="Thread-task", daemon=True)
        # t_task.start()
    else:
        tkinter.messagebox.showinfo('提示', '正在运行中')


def thread_task():
    try:
        # 启动守护线程 用于关闭干扰界面
        t_close = threading.Thread(target=close.close_interference, args=(), name="Thread-close", daemon=True)
        t_close.start()
        while True:
            # 关闭游戏teams
            game.exit_game()
            teams.exit_teams()
            user = teams.get_user_info()
            if len(user) != 2:
                break
            game_thread = threading.Thread(target=game_task, args=[user], name="Thread-game", daemon=True)
            game_thread.start()
            # 2小时强制退出
            start_time = time.time()
            while game_thread.is_alive():
                time.sleep(10)
                if time.time() - start_time >= 4800:
                    cf.terminate_thread(game_thread)
                    break
    finally:
        cf.run_task = True
        cf.RUN_TASK_PID = 0


def game_task(user):
    while True:  # 启动游戏-进入到主页
        if teams.login_teams(user[0], user[1]):
            print(user[0] + "----" + user[1])
            break
    game.start_game()  # 进入游戏到主界面
    task = cf.get("启动参数", "任务选项")
    for map_key in task.split(","):
        cf.FUNCTION_MAP.get(map_key)()
    teams.task_done(user, True)  # 添加完成标志


def thread_test_task():
    try:
        close.CURRENT = 'game'
        hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation")
        while hwnd == 0:
            time.sleep(5)
            hwnd = win32gui.FindWindow("DOAX VenusVacation", "DOAX VenusVacation")
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 624, 160, 1296, 759, win32con.SWP_SHOWWINDOW)
        t = threading.Thread(target=close.close_interference, args=(), name="Thread-close", daemon=True)
        t.start()
        task = cf.get("启动参数", "任务选项")
        for map_key in task.split(","):
            cf.FUNCTION_MAP.get(map_key)()
    finally:
        cf.test_task = True
        cf.TEST_TASK_PID = 0


def test_task():
    if cf.test_task:
        cf.test_task = False
        # task = threading.Thread(target=thread_test_task, args=(), name="Thread-close", daemon=True)
        # test_job = cf.Job(target=thread_test_task, args=(), name="Thread-close", daemon=True)
        process_test = multiprocessing.Process(target=thread_test_task, name="Process-test", daemon=True)
        process_test.start()
        cf.TEST_TASK_PID = process_test.pid
    else:
        tkinter.messagebox.showinfo('提示', '正在运行中')


# 主要界面
if __name__ == '__main__':
    multiprocessing.freeze_support()
    base = tkinter.Tk()
    base.geometry("320x200")
    base.wm_title("####")

    task_choose = tkinter.StringVar()
    e1 = tkinter.Listbox(base, listvariable=task_choose, width=20, height=7)
    task_choose.set(cf.get('启动参数', '任务选项').split(","))
    e1.place(x=20, y=20)

    btn = tkinter.Button(base, text="启动", command=run_task)
    btn.place(x=250, y=20)
    btn = tkinter.Button(base, text="测试", command=test_task)
    btn.place(x=250, y=50)
    btn = tkinter.Button(base, text="账号初始化", command=teams.init_account)
    btn.place(x=250, y=80)
    btn = tkinter.Button(base, text="暂停", command=cf.pause)
    btn.place(x=250, y=110)
    btn = tkinter.Button(base, text="恢复", command=cf.resume)
    btn.place(x=250, y=140)

    base.mainloop()
