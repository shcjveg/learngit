#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import constant
import socket
import json


class Communication_Thread(threading.Thread):
    def __init__(self, mainObj, countLock, stateLock):
        threading.Thread.__init__(self)
        self.mainObj = mainObj
        self.if_working = 1
        self.countLock = countLock
        self.stateLock = stateLock

    def run(self):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_socket.bind((constant.MY_IP, constant.MY_PORT))
        recv_socket.listen(1)
        if constant.NODE_ID == 0:
            while True:
                try:
                    send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                except:
                    print("waiting for connection")
                break
            data = {
                'EmptyCount': constant.MAX,
                'OnlineNode': constant.NODE_COUNT
            }
            json_data = json.dumps(data)
            send_socket.sendall(json.dumps(json_data).encode('utf-8'))
            send_socket.close()

        while True:

            coming_socket, addr = recv_socket.accept()
            recv_data = coming_socket.recv(1024)
            json_recv_data = json.loads(recv_data.decode('utf-8'))
            self.stateLock.acquire()
            if self.mainObj.workingState == 0:
                if json_recv_data['OnlineNode'] > 1:
                    # send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                    # send_socket.sendall(recv_data)
                    self.if_working = 0
                else:
                    print("请求关闭失败")
                    self.if_working = 1
            else:
                self.if_working = 1
            self.stateLock.release()

            if self.if_working == 0:
                send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                data2 = {
                    'EmptyCount': json_recv_data['EmptyCount'],
                    'OnlineNode': json_recv_data['OnlineNode'] - 1
                }
                json_data2 = json.dumps(data2)
                send_socket.sendall(json.dumps(json_data2).encode('utf-8'))
                send_socket.close()
            else:
                self.countLock.acquire()
                self.mainObj.emptyCount = json_recv_data['EmptyCount']
                self.mainObj.carCount = constant.MAX - self.mainObj.emptyCount
                # 考虑到可能无车也有出车请求
                if self.mainObj.readyOutCarCount <= self.mainObj.carCount:
                    self.mainObj.carCount = self.mainObj.carCount - self.mainObj.readyOutCarCount
                    self.mainObj.emptyCount = constant.MAX - self.mainObj.carCount
                    self.mainObj.readyOutCarCount = 0
                else:
                    self.mainObj.readyOutCarCount = self.mainObj.readyOutCarCount - self.mainObj.carCount
                    self.mainObj.emptyCount = constant.MAX
                    self.mainObj.carCount = 0
                if self.mainObj.readyInCarCount <= self.mainObj.emptyCount:
                    self.mainObj.carCount = self.mainObj.carCount + self.mainObj.readyInCarCount
                    self.mainObj.emptyCount = constant.MAX - self.mainObj.carCount
                    self.mainObj.readyInCarCount = 0
                else:
                    self.mainObj.readyInCarCount = self.mainObj.readyInCarCount - self.mainObj.emptyCount
                    self.mainObj.emptyCount = 0
                    self.mainObj.carCount = constant.MAX
                # count=self.mainObj.readyInCarCount-self.mainObj.readyOutCarCount
                # if count<=self.mainObj.emptyCount:
                #     self.mainObj.readyInCarCount=
                #     self.mainObj.emptyCount=self.mainObj.emptyCount-count
                # else:
                #     self.mainObj.emptyCount=0
                data3 = {
                    'EmptyCount': self.mainObj.emptyCount,
                    'OnlineNode': json_recv_data['OnlineNode']
                }
                self.countLock.release()
                json_data3 = json.dumps(data3)
                send_socket.sendall(json.dumps(json_data3).encode('utf-8'))
                send_socket.close()
