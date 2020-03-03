#将输入和输出源映射到GUI应用程序的弹出窗口
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText

class GuiOutput:
    font=('courier',9,'normal')
    def __init__(self,parent=None):
        self.text=None
        if parent:self.popupnow(parent) #先弹出或者第一次写入parent窗口
    def popupnow(self,parent=None):   #然后再到顶层窗口
        if self.text:return
        self.text=ScrolledText(parent )
        self.text.config(font=self.font)
        self.text.pack()
    def write(self,text):
        self.popupnow()
        self.text.insert(END,str(text))
        self.text.see(END)
        self.text.update()        #每行结束后更新画面
    def writelines(self,lines):   #有\n的行
        for line in lines:self.write(line)
class GuiInput:
    def __init__(self):
        self.buff=''
    def inputLine(self):
        line=askstring('GuiInput','Input a str')
        if line==None:return ''#针对各行弹出对话框
        else:return line+'\n' #取消按钮表示文件末尾,添加行结束的标记
    def read(self,bytes=None):
        if not self.buff: self.buff=self.inputLine()
        if bytes: #按照字节数读入
            text=self.buff[:bytes] #不分行
            self.buff=self.buff[bytes:]
        else:
            text=''  #持续读入，知道行末
            line=self.buff
            while line:
                text+=line
                line=self.inputLine() #直到cancle,eof或者''
        return text
    def readline(self):
        text=self.buff or self.inputLine()  #枚举文件读取方法
        self.buff=''
        return text
    def readlines(self):
        lines=[]  #读入所有的行
        while True:
            next=self.readline()
            if not next:break
            lines.append(next)
        return lines
def redirectionGuiFunc(func,*pargs,**kargs):
    import sys
    saveStreams=sys.stdin,sys.stdout  #讲函数中的流映射到弹出的窗口中
    sys.stdin=GuiInput()       #根据需要弹出对话框
    sys.stdout=GuiOutput()     #响应调用,创建新的弹出窗口
    sys.stderr=sys.stdout
    result=func(*pargs,**kargs) #这是阻塞调用
    sys.stdin,sys.stdout=saveStreams
def redirectedGuiShellCmd(command):
    import os
    input=os.popen(command,'r')
    output=GuiOutput()
    def reader(input,output):  #显示一个shell命令
        while True:  #标准输出
            line=input.readline() #在新的弹出式文本框组件中
            if not line: break  #调用readline时可能阻塞
            output.write(line)
        reader(input,output)

