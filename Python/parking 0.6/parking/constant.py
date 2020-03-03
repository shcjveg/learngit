#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Constant(object):
    def __init__(self):
        # 总车位数
        self.MAX = 30
        # 随机入车最短时间间隔
        self.MIN_IN_TIME = 1
        # 随机入车最长时间间隔
        self.MAX_IN_TIME = 5
        # 随机出车最短时间间隔
        self.MIN_OUT_TIME = 2
        # 随机出车最长时间间隔
        self.MAX_OUT_TIME = 6
        # 本地节点编号
        self.NODE_ID = 2
        # 本地IP
        self.MY_IP = '127.0.0.1'
        # 本地端口
        self.MY_PORT = 8899
        # 下一节点的IP
        self.NEXT_IP = "192.168.1.2"
        # 下一节点的端口
        self.NEXT_PORT = 8888
        # 上一节点的IP(不是必要的，引入这个是为了增强连接安全性，防它节点冒充)
        self.PREVIOUS_IP = "192.168.1.13"
