import configparser
import ctypes

import psutil

import game

run_task = True
test_task = True
RUN_TASK_PID = 0
TEST_TASK_PID = 0

cf = configparser.ConfigParser()
cf.read('./config.ini', encoding='utf-8')

WINDOW_MAP = {1: [951, 410],
              2: [945, 480],
              3: [942, 555],
              4: [944, 627],
              5: [950, 698],
              6: [944, 773]
              }
REWARDS_MAP = {1: [[1491, 733]],
               2: [[1333, 733], [1620, 732]],
               3: [[1263, 726], [1477, 726], [1676, 732]],
               4: [[1161, 727], [1367, 728], [1576, 729], [1786, 729]]
               }
FUNCTION_MAP = {"挑战赛-活动": game.challenge_active,
                "挑战赛-自定义": game.challenge_custom,
                "扭蛋": game.gashapon,
                "签到": game.check,
                "邮件": game.receive_mail,
                "任务": game.receive_task
                }
CHALLENGE_POINT_MAP = {
    '1': [1715, 553],
    '2': [1735, 625],
    '3': [1724, 701],
    '4': [1728, 767],
    '5': [1730, 843]
}


def terminate_thread(thread):
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def save_config(session, key, value):
    cf.set(session, key, value)
    with open('./config.ini', 'w', encoding='utf-8') as configfile:
        cf.write(configfile)


def get(session, key):
    return cf.get(session, key)


def pause():
    if RUN_TASK_PID != 0:
        proc = psutil.Process(RUN_TASK_PID)  # 传入子进程的pid，这里的pid用子进程的pid替换
        proc.suspend()
        print("RUN_TASK_PAUSE")
    if TEST_TASK_PID != 0:
        test_proc = psutil.Process(TEST_TASK_PID)  # 传入子进程的pid，这里的pid用子进程的pid替换
        test_proc.suspend()
        print("TEST_TASK_PAUSE")


def resume():
    if RUN_TASK_PID != 0:
        proc = psutil.Process(RUN_TASK_PID)  # 传入子进程的pid，这里的pid用子进程的pid替换
        proc.resume()
        print("TEST_TASK_RESUME")
    if TEST_TASK_PID != 0:
        test_proc = psutil.Process(TEST_TASK_PID)  # 传入子进程的pid，这里的pid用子进程的pid替换
        test_proc.resume()
        print("TEST_TASK_RESUME")
