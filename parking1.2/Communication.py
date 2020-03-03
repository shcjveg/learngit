import threading
import constant
import socket
import json
import time

from local_control import ControlTread
from readyInCarThread import readyInCarThread
from readyOutCarThread import readyOutCarThread


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

        while True:
            try:
                # print("123")
                send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                print(send_socket)
                print("---")
                # print("timeout")
                break
            except:
                print("waiting for connection")
                break
        readyInCarThread(self.mainObj, self.countLock).start()
        readyOutCarThread(self.mainObj, self.countLock).start()
        ControlTread(self.mainObj, self.stateLock).start()
        print("准备连接")
        coming_socket, addr = recv_socket.accept()
        print('连接成功', recv_socket)
        if constant.NODE_ID == 0:
            data = {
                'EmptyCount': constant.MAX,
                'OnlineNode': constant.NODE_COUNT
            }
            json_data = json.dumps(data)
            time.sleep(2)
            send_socket.sendall(json_data.encode('utf-8'))
            # send_socket.close()

        while True:

            recv_data = coming_socket.recv(1024)
            json_recv_data = json.loads(recv_data.decode('utf-8'))
            onlinenode = json_recv_data['OnlineNode']
            print("\n======" + str(json_recv_data) + "======\n")
            print("当前在线节点数：" + str(onlinenode))
            print("当前空车位数：" + str(json_recv_data['EmptyCount']))
            self.stateLock.acquire()
            if self.mainObj.Request == 0:
                if onlinenode > 1:
                    # send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                    # send_socket.sendall(recv_data)
                    self.if_working = 0
                    self.mainObj.workingState = 0
                    self.mainObj.Request = 2
                    # global onlinenode
                    onlinenode = onlinenode - 1
                    print("关闭成功")
                else:
                    print("只剩单个节点开启，请求关闭失败")
                    self.if_working = 1
                    self.mainObj.workingState = 1
            elif self.mainObj.Request == 1:
                self.mainObj.Request = 2
                onlinenode += 1
                self.if_working = 1
                self.mainObj.workingState = 1
            self.stateLock.release()

            if self.if_working == 0:
                # send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                data2 = {
                    'EmptyCount': json_recv_data['EmptyCount'],
                    'OnlineNode': onlinenode
                }
                json_data2 = json.dumps(data2)
                time.sleep(1)
                send_socket.sendall(json_data2.encode('utf-8'))
                # send_socket.close()
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
                    'OnlineNode': onlinenode
                }
                self.countLock.release()
                json_data3 = json.dumps(data3)
                # send_socket.connect((constant.NEXT_IP, constant.NEXT_PORT))
                time.sleep(1)
                send_socket.sendall(json_data3.encode('utf-8'))
                # send_socket.close()
