#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13
# @File    : readyOutCarThread.py
# @Software: PyCharm

import constant
import threading
import time
import random


class readyOutCarThread(threading.Thread):
    def __init__(self, mainObj, countLock):
        threading.Thread.__init__(self)
        self.mainObj = mainObj
        self.countLock = countLock

    def run(self):
        while True:
            if self.mainObj.workingState == 1:
                rand = random.randrange(constant.MIN_OUT_TIME, constant.MAX_OUT_TIME)
                # sleep以秒为单位
                time.sleep(rand)
                self.countLock.acquire()
                self.mainObj.readyOutCarCount += 1
                print("当前门准备出车数："+str(self.mainObj.readyOutCarCount))
                self.countLock.release()
            else:
                self.countLock.acquire()
                self.mainObj.readyOutCarCount = 0
                self.countLock.release()
