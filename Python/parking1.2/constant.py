#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 节点数量
NODE_COUNT = 3
# 总车位数
MAX = 30
# 随机入车最短时间间隔
MIN_IN_TIME = 1
# 随机入车最长时间间隔
MAX_IN_TIME = 5
# 随机出车最短时间间隔
MIN_OUT_TIME = 2
# 随机出车最长时间间隔
MAX_OUT_TIME = 6
# 本地节点编号
NODE_ID = 0
# 本地IP
MY_IP = '10.203.255.96'
# 本地端口
MY_PORT = 8899
# 下一节点的IP
NEXT_IP = "10.203.133.52"
# 下一节点的端口
NEXT_PORT = 8899
# 上一节点的IP(不是必要的，引入这个是为了增强连接安全性，防它节点冒充)
PREVIOUS_IP = "192.168.1.13"
