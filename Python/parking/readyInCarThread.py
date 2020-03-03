#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13
# @File    : readyInCarThread.py
# @Software: PyCharm


import threading
import time
import random
from main import countLock


class readyInCarThread(threading.Thread):
    def __init__(self, mainObj, constant):
        threading.Thread.__init__(self)
        self.mainObj = mainObj
        self.constant = constant

    def run(self):
        while True:
            rand = random.randrange(self.constant.MIN_IN_TIME, self.constant.MAX_IN_TIME)
            # sleep以秒为单位
            time.sleep(rand)
            countLock.acquire()
            self.mainObj.readyINCarCount += 1
            countLock.release()
