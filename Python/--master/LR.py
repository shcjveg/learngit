'''
LR(1)文法分析器
第一阶段 读取文法并记录产生式，完成ll,VT,VN
第二阶段 得到FIRST集
第三阶段 得到初步I
第四阶段 得到完整规范集
第五阶段 展示规范集
'''
import easygui as g
import os
from prettytable import PrettyTable


FIRST ={}                                       #存储FIRST集,key为非终结符，终结符。value为first集列表
FullSe=[]                                       #完整文法
ll={}                                           #存储，key = “终结符”，value = “产生式集合”
VT=[]                                           #终结符
VN=[]                                           #非终结符
StrI =[]                                        #验证新得到的I是否之前出现过
GO = {}                                         #{'原状态',[符号,到的状态]}
I ={}                                           #规范集
LI={}                                           #记录规范集中的左半部分
length = 0                                      #记录规范集的长度
F = []                                          #用于判断规范集中是否有可归约串
S =""                                           #记录开始符号
Table = {}                                      #记录分析表
Plist = [[],[],[],[],[]]                                      #记录分析过程
l=[]                                            #表头第一行

#读入文法
def ReadRules(path) :
    global  S,VN,VT
    vn=[]
    vt=[]
    global FullSe,ll,VN
    f = open(path, 'r')
    b = open("show.txt",'a+')                   #打印背景
    for line in f.readlines() :                 #逐行读取
        line = line.strip()
        FullSe.append(line)                     # 除掉换行符
        vn.append(line[0])
        if line[0] not in ll.keys() :           #存储产生式左端与右端
            ll[line[0]] = []
            ll[line[0]].append(line.split("->")[1])
        else :
            ll[line[0]].append(line.split("->")[1])
        for word in line.split("->")[1] :
            if word.isupper() is False :
                vt.append(word)
    FullSe.insert(0,FullSe[0][0]+"'->"+FullSe[0][0])           #拓广文法完整版
    c = '\n'.join(FullSe)
    b.write(c)
    title = g.msgbox(msg=c, title="拓广文法为", ok_button="确认无误，请点我！")
    S=vn[0]
    VN = list(set(vn))                          #去重
    VT = list(set(vt))
    b.close()
    os.remove("show.txt")

#找到FIRST集
def GetFIRST() :
    global ll
    li = list(ll)                   #将key值存到数组中，这样方便倒序访问,虽然ll是字典，但是li只会存储key值，字典无序
    for i in li :
        FIRST[i] = []               # 用列表存储FIRST集，因为会有多个
    judge  = True                   #用于判断FIRST集是否还在增长
    while judge == True :
        judge = False                   #先假设没有增长
        for i in reversed(li) :         #reversed()函数用于倒序访问列表，从下至上访问产生式
            for j in ll[i] :            #挨个访问产生式
                a = 1                   # 用于验证空集若所有的FIRST(Yj)均含有空字，j＝1，2，…，k，则把空字加到FIRST(X)中，先假设都含
                for k in range(len(j)) :            #若X→Y1Y2…Yk是一个产生式，Y1，…，Yi-1都是非终结符，而且，对于任何j，1<j<i-1，FIRST(Yj)都含有空集(即Y1…Yi-1)， 则把FIRST(Yi)中的所有非空集-元素都加到FIRST(X)中
                    if a == 0 :         #一旦不含空集就跳出循环
                        break
                    if j[k].isupper() :         #若是非终结符，把其FIRST集加入
                        for l in FIRST[j[k]]:
                            if l not in FIRST[i]:
                                judge = True
                                FIRST[i].append(l)
                        if '&' not in FIRST[j[k]]:  # 只要产生中有一个Yj不含空集，式子就不成立，就可停止循环
                            a = 0
                    else :               # 产生式X→a…，则把a加入到FIRST(X)中；若X→也是一条产生式，则把也加到FIRST(X)中
                        a = 0
                        if j[k] not in FIRST[i]:
                            judge = True
                            FIRST[i].append(j[k])
                if a == 1 and '&' not in FIRST[i]:  # 既满足原本无空集也满足所有产生式都含空集
                    judge = True
                    FIRST[i].append('&')
    for value in ll.values():               #终结符的FIRST集即为其本身
        for i in value :
            for j in i :
                if j.isupper() is False and j !="'" :
                    FIRST[j] =[j]

#若为A->a.Bc,#/...或A->a.B,#/.. 找出FIRST(右端)的集
def FindFIRST(str,stage) :
    s = str.index(',')
    Flist =[]
    if stage + 2 == s:   # E'=>.E,#  情况，即E后无其他字符
        for i in range(s+1,len(str)):
            Flist.append(str[i])
    else :
        judge = True                                    #判断各个首符集是否都含空集
        for i in range(stage+2,s):             #挨个访问字符
            for j in FIRST[str[i]] :                         #将FIRST集加入
                if j not in Flist :
                    Flist.append(j)
            if '&'not in FIRST[str[i]] :
                judge=False                             #只要有一个不含空集，就跳出
                break
        if judge == True :
            for k in range(s+1,len(str)):
                if k not in Flist :
                    Flist.append(k)
    if len(Flist) == 1 :
        answer = Flist[0]
    else :
        answer = ''.join(Flist)
    return answer
#加入项目,A->a.Bb中B的产生式
def AddDoc(I):
    i=0                                      #访问I并判断子集是否继续增长
    while i < len(I) :                          #当子集继续增长时，i继续访问直到访问完全
        str = I[i]
        stage = str.index(".")                  #得到.的位置
        if str[stage + 1] in VN  :               #如果.后面跟的是非终结符，即E->.FB，a
            right =FindFIRST(str,stage)
            for j in ll[str[stage + 1]] :       #将F中的产生式加入
                if (str[stage+1]+"->."+j+','+right) not in I :
                    for k in right :                            #FIRST集里可能有多个
                        I.append(str[stage+1]+"->."+j+','+k)
        i+=1
    return  I


#开始规范项目集的寻找
def GOTO(J,num) :
    global I,length,GO,StrI,FullSe
    Help = []  # 帮助判断归约-归约错误
    des = int()                             #用于记录GO的目的状态
    flag = []                               #标记符号是否已被访问
    GO[num] =[]                             #记录状态
    for i in range(0,len(J)):
        str_1 = J[i]
        stage_1 = str_1.index('.')             #找到'.'位置
        symbol = str_1[stage_1 + 1]               #找到'.'后面的符号
        if symbol not in flag and symbol != ',':             #未被访问才继续
            flag.append(symbol)             #标记
            NewI = []                       # 新的I
            NewI.append(str_1[:stage_1]+symbol+'.'+str_1[stage_1+2:])
            for j in range(i+1,len(J)):     #遍历后面相同在'.'后的符号
                str_2 = J[j]
                stage_2 = J[j].index('.')
                if str_2[stage_2 + 1] == symbol :
                    NewI.append(str_2[:stage_2]+symbol+'.'+str_2[stage_2+2:])
                                                     #这个阶段得到的NewI还需继续拓展，用Add，函数
            NewI =AddDoc(NewI)                    #完整的NewI
            if "".join(NewI) not in StrI :                          #检查NewI是否在之前出现过，若没出现过目的状态即为这个新产生的状态
                StrI.append("".join(NewI))
                I[length+1] = NewI
                length += 1
                des = length
            else :                                                  #若出现过，找到其出现的位置，并将目的状态加入
                des = StrI.index("".join(NewI))
            GO[num].append([symbol,des])
        elif symbol == "," :
                if str_1[stage_1-1] == S :                       #判断可归约串是否是开始符号，即acc
                    GO[num].append(["acc",1])
                else :
                    stage_2 = FullSe.index(str_1[:stage_1])         #不是的话[归约串对应的符号,产生式序号]
                    stage_str = str_1.index(",")
                    Conclude = str_1[stage_str+1:]
                    if ['C'+Conclude,stage_2] not in GO[num] :       #类似于同时出现F->E,# Q->E,#情况 归约-归约错误
                        if 'C'+Conclude in Help :
                            ShowDoc(J,num)
                            f = open("show.txt","r",encoding="utf-8")
                            g.msgbox('第'+str(num)+"个规范集存在归约-归约错误，不是LR（1）文法\n"+f.read(), title="提醒", ok_button="知道啦")
                            f.close()
                            os._exit(1)
                        else :
                            GO[num].append(['C'+Conclude,stage_2])
                            Help.append('C'+Conclude )


#优化项目规范集族展示
def ShowDoc(I,num):
    global  length
    show={}
    for i in I :                                                #访问I中的每个产生式
        if i.split(',')[0] not in show.keys() :                 #利用','将产生式与展望串分开
            show[i.split(',')[0]]=[]                            #展望串可能有多个，因此用列表存
            show[i.split(',')[0]].append(i.split(',')[1])
        else :                                                  #在之前出现过，就直接添加在后面
            show[i.split(',')[0]].append(i.split(',')[1])
    lis = []
    for key,value in show.items():
        str1 = key+','+'/'.join(value)
        lis.append(str1)
    f = open('show.txt','a',encoding="utf-8")
    f.write('I'+str(num)+":\n")
    f.write("\n".join(lis)+'\n')
    f.write("------------------------------\n")
    f.close()

#打印分析表
def PrintTable() :
    global GO,Table,l
    Flag = False                                                     #验证是否产生移进-归约冲突
    txt = str()
    f=open("show.txt","w",encoding="utf-8")
    y = PrettyTable(["  ","               ACTION            ","    GOTO    "])
    l.append("I")                                        #定义表头
    for i in range(0,len(VT)) :
        l.append(VT[i])
    l.append("#")
    for i in range(0,len(VN)) :
        l.append(VN[i])
    print(l)
    x = PrettyTable(l)                   #表头第二行
    for key,value in GO.items() :                                                         #表里添加数据
        str1 = []
        str1.append(str(key))
        for i in range(1,len(l)) :
            str1.append(" ")
        print(len(str1))
        for i in value :                #逐个访问key可以到达的所有状态与所经字符
            if i[0] in VT :                     #若项目[A->B·ab]属于Ik且GO(Ik, a)＝Ij， a为终结符，则置ACTION[k, a]为 “sj”。
                num = l.index(i[0])
                str1[num] = "S" + str(i[1])
            elif i[0] in VN :                  #若GO(Ik，A)＝Ij，则置GOTO[k, A]=j
                num = l.index(i[0])
                str1[num] = str(i[1])
            elif i[0] == "acc" :               #若项目[S'→S·, #]属于Ik，则置ACTION[k, #]为 “acc”。
                str1[l.index("#")] = "acc"
            elif i[0][0] == "C" :      #若项目[A→B·，a]属于Ik，则置ACTION[k, a]为 “rj”；其中假定A→B为文法的第j个产生式。
                num = l.index(i[0][1:])
                if str1[num]!=" ":            #判断是否存在多重入口
                    Flag = True
                    str1[num] +="/"+ "r" + str(i[1])
                else :
                    str1[num] = "r" + str(i[1])
        Table[key]=str1[1:]
        x.add_row(str1)
    if Flag == True :
        txt = "有多重入口，产生移进-归约冲突！不是LR(1)文法"
    else :
        txt = "分析表确认无误，请点我以继续！"
    f.write(str(y)+"\n")
    f.write(str(x))
    f.close()
    f = open("show.txt","r")
    g.msgbox(msg=f.read(), title="", ok_button=txt)
    f.close()

#分析过程
def Procedure(string) :
    global Table,Plist,l
    #string = "abab#"
    Plist[0].append(0)                          #过程列表的初始化
    Plist[1].append("0")
    Plist[2].append("#")
    Plist[3].append(string)
    Plist[4].append("初始化")
    stack_1 = []
    stack_2 = []
    stack_1.append('0')
    stack_2.append("#")
    Flag = 'A'                                 #用于验证是否得到acc
    stage = 0                                  #用于记录输入串访问位置
    ERROR = 0
    while Flag != 'acc' :
    #for i in range(0,10):
        command = Table[int(stack_1[-1])][l.index(string[stage])-1]              #注意一定要减一，表头第一个有I
        if command == "acc":
            #stack_1=['acc']
            stack_2.append(" ")
            Plist[4].append("acc:分析成功")
            Flag = "acc"
        elif command == " ":
            Plist[1].append("Failure ")
            Plist[2].append(" ")
            Plist[3].append(" ")
            Plist[4] = ""
            ERROR = 1
            break
        elif command[0] == "S" :                                       #移进
            stack_1.append(command[1])
            stack_2.append(string[stage])
            Plist[4].append("ACTION["+stack_1[-1]+","+string[stage]+"="+command+",状态"+command[1]+"入栈")
            stage+=1
        elif command[0] == "r" :                                       #归约
            left = FullSe[int(command[1])].split("->")[0]
            right = FullSe[int(command[1])].split("->")[1]
            for i in range (0,len(right)) :
                stack_1.pop()
                stack_2.pop()
            stack_1.append(Table[int(stack_1[-1])][l.index(left)-1])
            stack_2.append(left)
            Plist[4].append(command+":"+FullSe[int(command[1])]+"归约,GOTO("+stack_1[-1]+","+left+")="+command[1]+" 入栈")


        Plist[1].append("".join(stack_1))
        Plist[2].append("".join(stack_2))
        Plist[3].append(string[stage  :])

#展示分析表
def Procedure_Table() :
    global Plist
    string = e.get()         #得到用户标签输入
    Procedure(string)
    top = tk.Toplevel()  # 设计界面
    top.title('分析过程')  # 设计表格 五列，表头等
    t = ttk.Treeview(top, height=20, show="headings", columns=['0', '1', '2', '3','4'])
    t.column('0', width=80, anchor='center')
    t.column('1', width=80, anchor='w')
    t.column('2', width=80, anchor='w')
    t.column('3', width=80, anchor='center')
    t.column('4', width=200, anchor='center')
    t.heading('0', text='步骤')
    t.heading('1', text='状态')
    t.heading('2', text='符号')
    t.heading('3', text='输入串')
    t.heading('4', text='动作')
    t.pack()  # 放置标签
    for i in range(len(Plist[1])):
        value = [i, Plist[1][i], Plist[2][i], Plist[3][i],Plist[4][i]]
        t.insert('', 'end', value=value)

if __name__ == '__main__':
    path = g.enterbox(msg="请输入想要装载的文法路径(请将文法开始符号的产生式放在第一行！)", title="准备装载文法")
    #path = g.enterbox(msg="请输入想要分析的文件路径", title="准备装载文件")
    #path = "f://text4.txt"
    #path = g.enterbox(msg="请输入想要装载的文法路径(请将文法开始符号的产生式放在第一行！)", title="准备装载文法")
    f = open(path,'r',encoding="utf-8")
    title = g.msgbox(msg=f.read(), title="确认文法", ok_button="确认无误，请点我！")
    f.close()
    #读取文法
    ReadRules(path)

    #得到FIRST集
    GetFIRST()

    #构造规范集，定义I0
    stage = FullSe[0].index(">")
    s = FullSe[0]
    str1 = s[:stage+1]+"."+s[stage+1:]+","+"#"
    I[0]=[]
    I[0].append(str1)
    I[0]=AddDoc(I[0])

    #开始循环
    i=0
    StrI.append("".join(I[0]))      #用于验证新得到的I是否重复
    while i <= length :             #只要当前访问的不是最后一个就继续
        GOTO(I[i],i)                #寻找下一个状态
        ShowDoc(I[i],i)
        i+=1

    #添加GO过程
    f = open("show.txt", 'a', encoding="utf-8")
    for key,value in GO.items() :
        for i in value :
            if i[0][0] !="C" :
                f.write("GO("+str(key)+","+i[0]+")="+str(i[1])+"\n")
    f.close()

    #展示规范集
    f = open("show.txt", 'r', encoding="utf-8")
    IGO = g.msgbox(msg=f.read(), title="规范集", ok_button="确认无误，请点我！")
    f.close()

    #打印分析表
    PrintTable()


    import tkinter as tk
    from tkinter import *
    from tkinter import ttk

    window = tk.Tk()                # 第1步，实例化object，建立窗口window
    window.title('LR（1）文法分析')  # 第2步，给窗口的可视化起名字
    window.geometry('500x500')          # 第3步，设定窗口的大小(长 * 宽)
    frm1 = Frame(window)                #将window窗口分成两部分，一部分用来获取输入串
    frm2 = Frame(window)                #一部分用来展示FIRST，FOLLOW集,PAT

    var = StringVar()                   #           用于获取用户输入的字符串
    e = tk.Entry(frm1, width=30, textvariable=var)
    var.set('')
    e.grid(row=0, column=1, sticky=W)

    b2 = tk.Button(frm1, text='点击以分析输入串', width=12, height=1, command=Procedure_Table)  #给用户提供输入框，以及确认按钮
    b2.grid(row=0, column=2, sticky=W)

    t = tk.Text(frm2, height=100)           #用于展示规范集
    f = open('show.txt','r',encoding="utf-8")
    x = f.read()
    f.close()
    t.insert('insert',x)

    t.pack()                            #将三个标签置于窗口内
    frm1.pack(side=TOP)
    frm2.pack()
    #进行分析'''
    window.mainloop()                    #有这个函数才能看到界面
    os.remove("show.txt")
