# -*- coding: utf-8 -*-
import threading

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from src import teams, util
from src.core import config
from src.dm.dm_thread import DmThread

class Ui_Dialog(object):
    def __init__(self):
        self.worker = None

    def setupUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setObjectName("Dialog")
        Dialog.resize(475, 180)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 10, 115, 151))
        self.listWidget.setObjectName("listWidget")
        list = ["注册"]
        for i in range(len(list)):
            item = QtWidgets.QListWidgetItem()
            item.setText(_translate("Dialog", list[i]))
            item.setCheckState(Qt.Checked)
            self.listWidget.addItem(item)
        self.initButton = QtWidgets.QPushButton(Dialog)
        self.initButton.setGeometry(QtCore.QRect(370, 10, 75, 23))
        self.initButton.setObjectName("initButton")
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(370, 40, 75, 23))
        self.startButton.setObjectName("startButton")
        self.zantingButton = QtWidgets.QPushButton(Dialog)
        self.zantingButton.setGeometry(QtCore.QRect(370, 70, 75, 23))
        self.zantingButton.setObjectName("zantingButton")
        self.huifuButton = QtWidgets.QPushButton(Dialog)
        self.huifuButton.setGeometry(QtCore.QRect(370, 100, 75, 23))
        self.huifuButton.setObjectName("huifuButton")
        self.endButton = QtWidgets.QPushButton(Dialog)
        self.endButton.setGeometry(QtCore.QRect(370, 130, 75, 23))
        self.endButton.setObjectName("endButton")
        self.initButton.setText(_translate("Dialog", "初始账号"))
        self.startButton.setText(_translate("Dialog", "启动"))
        self.zantingButton.setText(_translate("Dialog", "暂停"))
        self.huifuButton.setText(_translate("Dialog", "恢复"))
        self.endButton.setText(_translate("Dialog", "结束"))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.startButton.clicked.connect(self.setUp)
        self.endButton.clicked.connect(self.stopGame)
        self.initButton.clicked.connect(self.initAccount)
        self.zantingButton.clicked.connect(self.zanTing)
        self.huifuButton.clicked.connect(self.huiFu)

    def setUp(self):
        self.worker = DmThread()
        self.worker.setName('DmThread')
        self.worker.setDaemon(True)
        self.worker.start()
        self.startButton.setEnabled(False)

    def stopGame(self):
        for item in threading.enumerate():
            print(item.getName())
        util.stop_thread_name('CloseThread')
        util.stop_thread_name('GameThread')
        util.stop_thread_name('DmThread')
        self.startButton.setEnabled(True)
        print('结束游戏')

    def zanTing(self):
        self.worker.pause()

    def huiFu(self):
        self.worker.resume()

    def initAccount(self):
        print('initAccount')
