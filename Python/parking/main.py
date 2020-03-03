#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13
# @File    : main.py.py
# @Software: PyCharm

import socket
import threading
from Map import Map, Node
from constant import Constant
from local_control import ControlTread
from readyInCarThread import readyInCarThread
from readyOutCarThread import readyOutCarThread
from tokenThread import tokenThread

countLock = threading.Lock()  # 声明锁
stateLock = threading.Lock()  # 状态锁


class MainObj:
    def __init__(self, map, constant):
        self.emptyCount = constant.MAX  # 当前空车位数
        self.carCount = 0  # 停车场内车数
        self.onlineNodeCount = map.nodeCount  # 当前在线节点数
        self.readyInCarCount = 0  # 该口申请进入车数
        self.readyOutCarCount = 0  # 该口申请离开车数
        self.canOff = 0  # 是否可以下班的状态
        self.workingState = 1  # 是否下班
        self.currentNodeId = constant.NODE_ID  # 本地节点id
        # self.currentIP = constant.IP  # 本地IP
        # self.currentPort = constant.PORT  # 本地端口


if __name__ == "__main__":
    constant = Constant()
    node1 = Node(0, 'ip', 'port')
    node2 = Node(1, 'ip', 'port')
    systemMap = Map()
    systemMap.add(node1)
    systemMap.add(node2)
    mainObj = MainObj(systemMap, constant)
    # TODO
    #  socket
    # 创建 socket 对象
    socketList = []
    for i in range(mainObj.onlineNodeCount):
        socketList.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        socketList[i].bind((systemMap.nodeList[i].ip, systemMap.nodeList[i].port))
        socketList[i].listen(5)

    tokenThread().start()

    if mainObj.currentNodeId == 0:
        # send token to next node and socket
        # TODO send token


    readyInCarThread(mainObj, constant).start()
    readyOutCarThread(mainObj, constant).start()
    ControlTread(mainObj, stateLock).start()
