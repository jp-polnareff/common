import ctypes
import inspect
import threading


def stop_thread_name(name):
    for item in threading.enumerate():
        if item.getName() == name:
            stop_thread(item)
            print(name + '线程结束')


def async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        return
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    async_raise(thread.ident, SystemExit)