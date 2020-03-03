#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13
# @File    : main.py.py
# @Software: PyCharm


import threading
import constant
from local_control import ControlTread
from readyInCarThread import readyInCarThread
from readyOutCarThread import readyOutCarThread
from Communication import Communication_Thread

countLock = threading.Lock()  # 声明锁
stateLock = threading.Lock()  # 状态锁


class MainObj:
    def __init__(self):
        self.emptyCount = constant.MAX  # 当前空车位数
        self.carCount = 0  # 停车场内车数
        # self.onlineNodeCount = map.nodeCount  # 当前在线节点数
        self.readyInCarCount = 0  # 该口申请进入车数
        self.readyOutCarCount = 0  # 该口申请离开车数
        self.Request = 2  # 外部的请求，1表示上班请求，0表示下班请求,2表示无请求
        self.workingState = 1  # 当前状态，1：上班
        self.currentNodeId = constant.NODE_ID  # 本地节点id
        # self.currentIP = constant.IP  # 本地IP
        # self.currentPort = constant.PORT  # 本地端口


if __name__ == "__main__":
    # node1 = Node(0, 'ip', 'port')
    # node2 = Node(1, 'ip', 'port')
    # systemMap = Map()
    # systemMap.add(node1)
    # systemMap.add(node2)
    # TODO
    #  socket
    # 创建 socket 对象
    # socketList = []
    # for i in range(mainObj.onlineNodeCount):
    #     socketList.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    #     socketList[i].bind((systemMap.nodeList[i].ip, systemMap.nodeList[i].port))
    #     socketList[i].listen(5)

    # 我觉得不需要Socket队列，一个监听上家的Socket和一个发送给下家的Socket就可以了
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((constant.MY_IP,constant.MY_PORT))
    # server.listen(1)
    # #
    # next = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # while 1:
    #     try:
    #         next.connect((constant.NEXT_IP,constant.NEXT_PORT))
    #         print("连接成功")
    #         break
    #     except:
    #         print("连接失败，重新与下游节点发起连接...")
    # prev,address = server.accept()
    # if(not address==constant.PREVIOUS_IP):
    #     print("实际连接的上游节点"+address+"与本地记录ip不相符，请注意查验！")

    mainObj = MainObj()

    readyInCarThread(mainObj, countLock).start()
    readyOutCarThread(mainObj, countLock).start()
    ControlTread(mainObj, stateLock).start()
    Communication_Thread(mainObj, countLock, stateLock).start()

    # readyInCarThread.join()
    # readyOutCarThread.join()
    # ControlTread.join()
    # Communication_Thread.join()
    # print("程序结束")
