#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/13
# @File    : Map.py
# @Software: PyCharm


class Map:
    def __init__(self):
        self.nodeList = []
        self.nodeCount = 0

    def add(self, node):
        self.nodeList.append(node)
        self.nodeCount += 1


class Node:
    def __init__(self, nodeId, ip, port):
        self.nodeId = nodeId
        self.ip = ip
        self.port = port
