import random
import time

from pydmsoft.dm import DM


class DmUtil:
    def __init__(self, dm: DM):
        self.dm = dm

    def pullTo(self, x1, y1, x2, y2):
        self.dm.EnableBind(0)
        self.dm.MoveTo(x1, y1)
        time.sleep(1)
        self.dm.LeftDown()
        time.sleep(1)
        self.dm.MoveTo(x2, y2)
        time.sleep(1)
        self.dm.LeftUp()
        self.dm.EnableBind(1)

    def existPic(self, x1, y1, x2, y2, pic_name, delta_color='202020', sim=0.8, dir=0):
        res = self.findPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
        if res[0] < 0:
            return False
        return True

    def findPicLeftDoubleClick(self, x1, y1, x2, y2, pic_name, delta_color='202020', sim=0.8, dir=0):
        res = self.findPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
        if res[0] < 0:
            return False
        self.moveToAndLeftDoubleClick(res[1], res[2])
        return True

    def findPicLeftClickOffset(self, x1, y1, x2, y2, pic_name, delta_color='202020', sim=0.9, dir=0, x=0, y=0):
        res = self.findPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
        if res[0] < 0:
            return False
        self.moveToAndLeftClick(res[1] + x, res[2] + y)
        return True

    def findPicLeftClick(self, x1, y1, x2, y2, pic_name, delta_color='202020', sim=0.9, dir=0):
        res = self.findPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
        if res[0] < 0:
            return False
        self.moveToAndLeftClick(res[1], res[2])
        return True

    def findPic(self, x1, y1, x2, y2, pic_name, delta_color='202020', sim=0.9, dir=0):
        res = self.dm.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)
        print(res)
        return res.initial_result

    def findStrFastExS(self, x1, y1, x2, y2, str, color, sim):
        res = self.dm.FindStrFastExS(x1, y1, x2, y2, str, color, sim)
        result = []
        if res != '':
            substrings = res.split("|")
            for substring in substrings:
                parts = substring.split(',')
                x = int(parts[1])
                y = int(parts[2])
                result.append((x, y))
        sorted_result = sorted(result, key=lambda item: item[0])
        return sorted_result

    def rightClick(self):
        self.dm.RightClick()
        time.sleep(random.uniform(0.5, 1.5))

    def findColorLeftClick(self, x1, y1, x2, y2, color, sim, dir):
        res = self.findColor(x1, y1, x2, y2, color, sim, dir)
        if res[0] <= 0:
            return False
        self.moveToAndLeftClick(res[1], res[2])
        return True

    def findColor(self, x1, y1, x2, y2, color, sim, dir):
        res = self.dm.FindColor(x1, y1, x2, y2, color, sim, dir)
        return res.initial_result

    def findWindow(self, class_name, title_name):
        res = self.dm.FindWindow(class_name, title_name)
        return int(res.__str__())

    def findWindowSure(self, class_name, title_name):
        res = self.dm.FindWindowSuper(class_name, 2, 0, title_name, 0, 0)
        return int(res.__str__())

    def setWindowPos(self, hwnd, x, y, height, length, state):
        self.dm.MoveWindow(hwnd, x, y)
        self.dm.SetWindowSize(hwnd, height, length)
        self.dm.SetWindowState(hwnd, state)
        time.sleep(3)

    def bindWindow(self, hwnd, display, mouse, keypad, mode):
        return self.dm.BindWindow(hwnd, display, mouse, keypad, mode)

    def moveToAndLeftClick(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.LeftClick()
        time.sleep(random.uniform(0.5, 1.5))

    def moveToAndLeftDoubleClick(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.LeftDoubleClick()
        time.sleep(random.uniform(1, 3))

    def moveCommon(self, ):
        self.dm.MoveTo(313, 972)

    def existStr(self, x1, y1, x2, y2, str, color, sim):
        res = self.findStrE(x1, y1, x2, y2, str, color, sim)
        return res[0] == 0

    def findStrE(self, x1, y1, x2, y2, str, color, sim):
        res = self.dm.FindStrFastE(x1, y1, x2, y2, str, color, sim)
        parts = res.__str__().replace('\'', '').split('|')
        return tuple(map(int, parts))

    def findStrEAndLeftClick(self, x1, y1, x2, y2, str, color, sim):
        res = self.findStrE(x1, y1, x2, y2, str, color, sim)
        if res[0] == -1:
            return False
        self.moveToAndLeftClick(res[1], res[2])
        return True

    def findStrEAndLeftClickOffset(self, x1, y1, x2, y2, str, color, sim, x=0, y=0):
        res = self.findStrE(x1, y1, x2, y2, str, color, sim)
        if res[0] == -1:
            return False
        self.moveToAndLeftClick(res[1] + x, res[2] + y)
        return True

    def findStrEAndLeftDoubleClick(self, x1, y1, x2, y2, str, color, sim):
        res = self.findStrE(x1, y1, x2, y2, str, color, sim)
        if res[0] == -1:
            return False
        self.moveToAndLeftDoubleClick(res[1], res[2])
        return True
