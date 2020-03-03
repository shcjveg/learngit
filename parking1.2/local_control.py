#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import time


# from main import stateLock


class ControlTread(Thread):
    def __init__(self, mainObj, stateLock):
        super().__init__()
        self.mainObj = mainObj
        self.stateLock = stateLock

    def run(self):
        while True:
            if self.mainObj.workingState == 1:
                command = input("当前门是开启状态，是否请求将门关闭？(y/n)\n")
                if command == "y":
                    self.stateLock.acquire()
                    self.mainObj.Request = 0
                    self.stateLock.release()
                    print("正在尝试关闭...")
                    while self.mainObj.workingState == 1:
                        pass
                    print("成功关闭！")

                    # todo jia dengdai
            else:
                command = input("当前门是关闭状态，是否请求将门开启？(y/n)\n")
                if command == "y":
                    self.stateLock.acquire()
                    self.mainObj.Request = 1
                    self.stateLock.release()
                    print("正在尝试开启...")
                    while self.mainObj.workingState == 0:
                        pass
                    print("成功开启！")
