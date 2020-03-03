#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
# from main import stateLock


class ControlTread(Thread):
    def __init__(self, mainObj, stateLock):
        super().__init__()
        self.mainObj = mainObj
        self.stateLock = stateLock

    def run(self):
        while True:
            if self.mainObj.workingState == 1:
                command = input("是否将门关闭？(y/n)")
                if command == "y":
                    if self.mainObj.canOff:
                        self.stateLock.acquire()
                        self.mainObj.workingState = 0
                        self.stateLock.release()
                        print("已将门关闭")
            else:
                command = input("是否将门开启？(y/n)")
                if command == "y":
                    self.stateLock.acquire()
                    self.mainObj.workingState = 0
                    self.stateLock.release()
                    print("已将门关闭")
