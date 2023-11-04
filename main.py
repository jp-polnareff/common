# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import win32gui
from PyQt5.QtWidgets import QApplication, QWidget

from src.qt import Ui_Dialog


def list_all_windows():
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            print(f"窗口class: {win32gui.GetClassName(hwnd)} 窗口标题: {window_title}, 句柄: {hwnd}")

    win32gui.EnumWindows(callback, None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QWidget()
    w = Ui_Dialog()
    w.setupUi(form)
    form.move(14, 820)
    form.show()
    sys.exit(app.exec_())
