'''
编译原理 LL(1)实验------周余
（2019.10.10完成）第一阶段 利用字典储存产生式,列表存储非终结符，KEY=终结符 ，VALUE=右端产生式以'|'分开的列表。例如 S→Qc|c 存为'S': ['Qc', 'c']
（2019.10.11完成）第二阶段 完成左递归的消除
                        子阶段1.消除间接左递归，主要利用对列表的insert函数和remove函数（2019.10.11完成）
                        子阶段2.消除直接左递归，主要利用新建一个字典，列表的append函数，注意字典不能在迭代过程中改变size大小。（2019.10.11完成）\
（2019.10.11完成）第三阶段 消除回溯,主要利用append函数，也需新建一个字典，左因子一定在最左端
（2019.10.11完成）第四阶段 找出FIRST集，将key值存入列表中，方便倒序访问，只需list（）即可。然后从上到下依次寻找。
 (2019.10.12完成）第五阶段 找出FOLLOW集，只看右端产生式，逐个字符看，注意空集以及多次循环同步直至集合不再增长
 (2019.10.12完成) 第六阶段 构造分析表，用到list，注意初始化，以及左端FOLLOW集的加入条件
 (2019.10.13完成) 第七阶段 分析输入串
 (2019.10.14完成) 第八阶段 界面展示
'''
'''
S→Qc|c
Q→Rb|b
R→Sa|a
主要用到的数据结构：字典，列表
函数 列表的split(),append(),pop()，remove(),insert()
    字符串的 '+'直接组合以及join()函数
'''
VN = []  # 存储非终结符
VT = []  # 存储终结符
FIRST={} # FIRST集
FOLLOW = {} #FOLLOW集
Twice = 0 #判断是否有多重定义入口

import easygui as g
#读取文法子函数
def ReadRules(path):
    f = open(path,'r')
    ll={}                                                        #存储文法
    for line in f.readlines() :
        if line[0] not in ll.keys() :                           #S→Qc|c
            ll[line[0]] = []                                     #VALUE用列表存储
        line = line.strip()                                      #消除换行符
        if '|' in line.split('->')[1]:                          #判断是否多重选择
            li = line.split('->')[1].split('|')                 #利用'→'将终结符与产生式分开，利用'|'将产生式的多种入口分开
            for i in li :                                       #如若不如此存，会存诚二维数组例如[['+TG', '—TG'], 'ε']
                ll[line[0]].append(i)
                for j in i :
                    if j.isupper() is False and j != '&' :     #得到VT
                        VT.append(j)
        else :
            ll[line[0]].append(line.split('->')[1])             #只有一种选择，直接加入列表
            for j in line.split('->')[1]:
                if j.isupper() is False and j != '&':
                    VT.append(j)
        if line[0] not in VN :                                  #去重，可用set（）的性质
            VN.append(line[0])
    return  ll                                                #将文法成功用字典存储，key=终结符；value=产生式以‘|’分开的列表

                                                            #存储形式举例：{"G":['+TG','-TG','&']}
#消除左递归子函数
def DelLeft(ll) :
    #消除间接左递归,进行替换处理
    a = 1
    Left = False                                                   #判断是否进行了左递归
    while (a ==1 ) :                                                        #需要多次调整
        a=0                                                                 #假设没有进行调整
        for key,value in ll.items():                                        #以键值对形式逐个访问字典
            lenth = 0                                                       #对非终结符进行排序，从上到下的顺序是从低到高
            for i in value :                                                #逐个访问value里的列表值,挨个得到产生式的右端,如S→Qc|c ，i=Qc，c
                if i[0] in VN and VN.index(i[0]) < VN.index(key):           #如果高->低，进行操作
                     a=1                                                    #一旦进行调整马上记录
                     Left=True
                     for j in ll[i[0]] :                                    #将低的产生式逐个替换并插入高的产生式,如R→Sa|a变为R→Qca|ca|Sa|a
                        value.insert(lenth,j+i[1:len(i)])                   #注意是插入不是append，这样可直接从首开始插入，更直观
                        lenth += 1
                     value.remove(i[0]+i[1:len(i)])                         #将替换前的产生式删除，如R→Qca|ca|Sa|a变为R→Qca|ca|a
    #消除直接左递归
    real_11={}                                                              #必须使用另一个字典来进行转化，字典不能在迭代访问过程中改变大小
    for key,value in ll.items() :
        if value[0][0] == key :                                             #判断是否需要进行直接左递归
            Left = True
            real_11[key]=[]
            real_11[key+'\'']=[]
            for i in value :                                               #以E->E+T|T
                if i[0] == key :                                            #找到第一个字符与产生式右端的非终结符相等的产生式，进行左递归
                   real_11[key+'\''].append(i[1:len(i)]+key+'\'')           #E'→+TE'
                   VN.append(key+'\'')
                   FOLLOW[key+"\'"]=[]
                else :
                    real_11[key].append(i+key+'\'')                         #E→TE'
            real_11[key + '\''].append("&")                                 #进行左递归后，不要忘记空字
        else :
            real_11[key]=value                                               #若是不用进行直接左递归，则直接传递相同键值对
    return real_11,Left

#消除回溯子函数
def DelBack(ll) :
    real_ll={}             #必须使用另一个字典来进行转化，字典不能在迭代访问过程中改变大小
    judge = 1
    while judge == 1:      #需要多次循环检查新的产生式是否还有新的左因子
        judge = 0           #假设未进行调整
        for key,value in ll.items() :
            counts={}                                                           #counte用于将产生式右端按首字母分类，例如T->bR|b|c 即可转化为counte[b]={bR,b};counts[c]={c}
            a = 0                                                               #用于判断是否有左因子存在
            for i in value :
                if i not in counts.keys() :
                    counts[i[0]]=[]
                    counts[i[0]].append(i)
                else :
                    a = 1                                                       #首字母不止一次出现
                    judge = 1
                    counts[i[0]].append(i)
            if a == 0 :                                                         #若产生式无左因子存在，直接传递即可
                real_ll[key] = value
            else :                                                              #否则，需进行下一步操作，以T->bR|b|c 为例
                real_ll[key] = []
                real_ll[key+'\''] = []
                for key1,value1 in counts.items() :
                    if len(value1) == 1 :                                       #将不含左因子的字符串直接写入
                        real_ll[key].append(value1[0])                           #T->C
                    else :                                                      #将含左因子的字符串右端提取出来，产生新的产生式
                        real_ll[key].append(key1+key+"\'")                      #T->bT'
                        for j in value1 :
                            if len(j) == 1:                                     #T'->R|空字
                                real_ll[key+'\''].append('&')                  #一定要注意空集，counte[b]={bR,b};counts[c]={c}
                            else :
                                real_ll[key+'\''].append(j[1:len(j)])
        ll = real_ll
    return real_ll

#找到文法中的FIRST集
def FindFIRST(ll) :
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
                        str = ""
                        if j[k+1] == "'"  :       #需要判断后面是否有'
                            str = j[k]+"'"
                        else :
                            str = j[k]
                        for l in FIRST[str]:
                            if l not in FIRST[i]:
                                judge = True
                                FIRST[i].append(l)
                        if '&' not in FIRST[str]:  # 只要产生中有一个Yj不含空集，式子就不成立，就可停止循环
                            a = 0
                    elif j[k] != "'":               # 产生式X→a…，则把a加入到FIRST(X)中；若X→也是一条产生式，则把也加到FIRST(X)中
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

#找到文法中的FOLLOW集
def FindFOLLOW(ll) :
    for i in VN:
        FOLLOW[i] = []
    FOLLOW[VN[0]].append("#")               # 对于文法的开始符号S，置＃于FOLLOW(S)中
    a = 1                                   #进行多次循环直至集合不再增长,否则FOLLOW集不正确，亲自验证
    while a == 1:
        a = 0                               #假设没有增长
        for key,value in ll.items():
            for i in value :                    #获得右端每个产生式中的字符串
                save = 1                        #FIRST集中是否有空字，一旦后续的没有空字就置零,例如F->EG，从最后一位开始相当于是有都有空字
                for j in range(len(i)-1,-1,-1) :   #挨个挨个倒序字符的访问
                    str = ""
                    if i[j] in FOLLOW.keys():
                        if j == len(i)-1 or i[j+1] != "'":  #判断是否是F'
                                str = i[j]
                        else :
                            str = i[j]+ "'"
                        if save ==1 and str!=key:                           #若A→aB是一个产生式，或A->aBC是一个产生式而C含空集 (即空集属于FIRST()),则把FOLLOW(A)加至FOLLOW(B)中。
                            for k in FOLLOW[key] :                          #将FOLLOW(A)加入FOLLO(B)
                                if k not in FOLLOW[str]:
                                    a =1
                                    FOLLOW[str].append(k)
                        if j !=len(i)-1 and i[j+1] != "'":                       #若A→aBC是一个产生式，则把FIRST(C)\{空集}加至FOLLOW(B)中；
                            str2 = ''
                            if j+2 < len(i) and i[j+2]=='\'':           #F->EF'
                                str2 = i[j+1] +'\''
                            else :
                                str2 = i[j+1]
                            for k in FIRST[str2] :
                                if k != '&' and k not in FOLLOW[str]:
                                    a=1
                                    FOLLOW[str].append(k)
                        if '&' not in FIRST[str] :         #只要有一个字符的FIRST集不含空集，那么后续均无法使用第二公式
                                save = 0
                    elif  i[j] != '\'' :  #若是非终结符，也是无空字的意思
                        save = 0

#打印FIRST,FOLLOW集
def PrintFIRSTFOLLOW():
    li =[]                                                                 #用于写入文件
    lr =[]
    f = open('show.txt', 'a+', encoding="utf-8")
    for i in  VN :
        li.append("FIRST("+i+")"+"= {"+",".join(FIRST[i])+"}")     #组装存于字典value里的列表
        lr.append("FOLLOW("+i+")"+"= {"+",".join(FOLLOW[i])+"}")
    f.write("-----------------------FIRST集-----------------------\n")
    f.write("\n".join(li))
    f.write("\n-----------------------FOLLOW集-----------------------\n")
    f.write("\n".join(lr))
    f.close()

#得到分析表
def GetTable(ll):
    global Twice                                                  #重点，否则无法改变全局值
    VT.append("#")
    AList = [[0 for i in range(len(VT))] for j in range(len(VN))] # 构造分析表，初始值为0
    for key,value in ll.items() :
        for i in value :
            line = key+"->"+i                 #将字典中二点key与value进行组装{'G':['TG','FS']|
            judge = 1                          #用于判断FIRST集里是否有空字，因从第一个字符开始，先假设有空字。
            for j in i :
                for k in FIRST[j] :                                 #对每个终结符a属于FIRST(右端产生式)，把产生式 加至M[A，a]中
                    if k != '&' :
                        if AList[VN.index(key)][VT.index(k)] != 0 and AList[VN.index(key)][VT.index(k)] != line:  #判断是否已经存在式子，即有多重入口
                            AList[VN.index(key)][VT.index(k)] += "/"+line   #F->TG/F->JK
                            Twice = 1
                        else :
                            AList[VN.index(key)][VT.index(k)] = line
                if  '&'not in FIRST[j] :                            #旦FIRST集里无空集，立刻停止寻找
                    judge = 0
                    break                                          #例子G->FG|&
            if judge == 1 :                                         #若空集属于FIRST(右端产生式)，则对任何b属于FOLLOW(A)把产生式加至M[A，b]中。
                for j in FOLLOW[key] :
                    if AList[VN.index(key)][VT.index(j)] != 0 and AList[VN.index(key)][VT.index(j)] != line  :#判断是否已经存在式子，即有多重入口
                        AList[VN.index(key)][VT.index(j)] += "/"+ line  #F->TG/F->JK
                        Twice = 1
                    else :
                        AList[VN.index(key)][VT.index(j)] = line
    return AList

#打印分析表
def PrintTable(Alist) :
    f = open('show.txt', 'a+', encoding="utf-8")        #否则乱码
    f.write("\n\n-----------------------PAT-----------------------\n")                 #分析表的格式化
    f.write("{:<8}".format(" "))
    for i in VT :                               #写入终结符
        f.write("{:<8}".format(i))
    f.write("\n")
    for i in range(len(VN)) :
        f.write("{:<8}".format(VN[i]))
        for j in range(len(VT)) :
            f.write("{:<8}".format(Alist[i][j]))
            if j == len(VT)-1 :
                f.write("\n")
    f.close()
    info =""                                                #给用户展示界面
    if Twice == 1:
        f = open('show.txt', 'r', encoding="utf-8")
        title = g.msgbox(msg=f.read(), title="确认分析表", ok_button="分析表含多重入口，不是LL（1）文法！")
        f.close()
    else :
        f = open('show.txt', 'r', encoding="utf-8")
        title = g.msgbox(msg=f.read(), title="确认分析表", ok_button="分析表不含多重入口，是LL（1）文法，请点我继续！")
        f.close()

def Procedure(Alist,str) :
    ProcedureList = [ [], [], [], []]  # 记录过程的表格
    stack = []                                                          #初始化栈，Python无栈，用List代替，append()函数相当于是push
    stack.append("#")
    stack.append(VN[0])
    length = 0                  #记录所输入的字符串分析到哪里了
    Flag = True                                                             #代表是否分析完毕
    Error = 0                                                               #代表是否出现错误
    ProcedureList[0].append("".join(stack)) #表格的初始化
    ProcedureList[1].append(str[length:len(str)])
    ProcedureList[2].append(" ")
    ProcedureList[3].append("初始化")
    while Flag:
        word = stack.pop()                                       #弹出栈最上方元素
        if word == '#' :                                        #栈已经到“#”
            ProcedureList[2].append(" ")
            ProcedureList[1].append(" ")
            if word == str[length] :                            #如果需分析的字符串也到'#'，则成功，否则失败
                Flag = False
                ProcedureList[3].append("分析成功")
                print("分析成功")
            else :
                Error = 1
                print("error!")
        elif word in VT:                                   #如果最上方元素是终结符，需分析的字符串所到位置也是此终结符，则进行下一个字符的分析，否则错误
            ProcedureList[2].append(" ")
            if word == str[length] :
                ProcedureList[3].append("GETNEXT(I) ")
                length+=1
            else :
                Error = 1
                print("error")
        elif Alist[VN.index(word)][VT.index(str[length])] !=0 :  #如果是非终结符，进行查表，如果有产生式存在，进行下一步，否额错误
            ProcedureList[2].append(Alist[VN.index(word)][VT.index(str[length])])
            str1 = Alist[VN.index(word)][VT.index(str[length])].split('->')[1]   #得到产生式的右部
            if str1 == '&' :                                #如果是空字，直接pop
                ProcedureList[3].append("POP")
            else :                                           #既有Pop，也有push
                pstr = ''                               #压入的产生式倒过来，不能直接字符串反转，因为F'会被变成'F
                for i in range(len(str1)-1,-1,-1):       #倒序访问压入栈，注意F'
                    if str1[i]!='&' and str1[i]!='\'':
                        if i+1<len(str1):
                            if str1[i+1] == '\'':
                                stack.append(str1[i]+'\'')
                                pstr += str1[i]+'\''
                            else :
                                stack.append(str1[i])
                                pstr += str1[i]
                        else :
                            stack.append(str1[i])
                            pstr+=str1[i]
                ProcedureList[3].append("pop,"+"push("+pstr+")")
        else :
            Error =1
        if Error == 1 :                                         #一旦发现错误停止分析
            ProcedureList[0].append("")
            ProcedureList[1].append("")
            ProcedureList[2].append(" ")
            ProcedureList[3].append("分析失败")
            break
        ProcedureList[0].append("".join(stack))
        ProcedureList[1].append(str[length:len(str)])
    return ProcedureList

#打印分析界面
def procedure_table():
    string = e.get()            #得到用户标签的输入
    ProcedureList = Procedure(Alist,string)#进行分析
    top = tk.Toplevel()         #设计界面
    top.title('分析过程')           #设计表格 五列，表头等
    t = ttk.Treeview(top, height=20, show="headings",columns=['0', '1', '2', '3', '4'])
    t.column('0', width=80, anchor='center')
    t.column('1', width=80, anchor='w')
    t.column('2', width=80, anchor='e')
    t.column('3', width=80, anchor='center')
    t.column('4', width=100, anchor='center')
    t.heading('0', text='步骤')
    t.heading('1', text='分析栈')
    t.heading('2', text='剩余输入串')
    t.heading('3', text='所用产生式')
    t.heading('4', text='动作')
    t.pack()        #放置标签
    for i in range(len(ProcedureList[0])):
        value = [i,ProcedureList[0][i],ProcedureList[1][i],ProcedureList[2][i],ProcedureList[3][i]]
        t.insert('','end',value=value)

if __name__ == '__main__':
    path = g.enterbox(msg="请输入想要装载的文法路径(请将文法开始符号的产生式放在第一行！)", title="准备装载文法")                       #获取用户输入路径
    #读取文法
    ll={}
    f = open(path,'r')
    title = g.msgbox(msg=f.read(), title="确认文法", ok_button="确认无误，请点我！")
    ll  = ReadRules(path)
    f.close()


    #消除左递归

    ll,Left = DelLeft(ll)
    li=[]
    if Left == True :
        for key,value in ll.items() :
            if len(value) == 1 :
                line = key + '->'+ ''.join(value)
            else :
                line = key +'->'+'|'.join(value)
            li.append(line)
        title = g.msgbox(msg="此文法含左递归，不是LL（1）文法，消除左递归后的文法为\n" + '\n'.join(li), title="确认文法", ok_button="如果想继续使用修改后的文法，请点我！")
        #title = g.msgbox(msg="此文法含公共左因子，反复提取公共左因子后的文法为\n" + '\n'.join(li), title="确认文法",ok_button="如果想继续使用修改后的文法，请点我！")
    #消除回溯
    ll = DelBack(ll)

    #得到FIRST集
    FindFIRST(ll)

    #得到FOLLOW集
    FindFOLLOW(ll)
    PrintFIRSTFOLLOW()


    #得到分析表
    Alist = GetTable(ll)
    PrintTable(Alist)

    import tkinter as tk
    from tkinter import *
    from tkinter import ttk

    window = tk.Tk()                # 第1步，实例化object，建立窗口window
    window.title('LL（1）文法分析')  # 第2步，给窗口的可视化起名字
    window.geometry('500x500')          # 第3步，设定窗口的大小(长 * 宽)
    frm1 = Frame(window)                #将window窗口分成两部分，一部分用来获取输入串
    frm2 = Frame(window)                #一部分用来展示FIRST，FOLLOW集,PAT

    var = StringVar()                   #           用于获取用户输入的字符串
    e = tk.Entry(frm1, width=30, textvariable=var)
    var.set('')
    e.grid(row=0, column=1, sticky=W)

    b2 = tk.Button(frm1, text='点击以分析输入串', width=12, height=1, command=procedure_table)  #给用户提供输入框，以及确认按钮
    b2.grid(row=0, column=2, sticky=W)

    t = tk.Text(frm2, height=100)           #用文本框展示FIRST，FOLLOW集以及PAT
    f = open('show.txt','r',encoding="utf-8")
    x = f.read()
    f.close()
    t.insert('insert',x)

    t.pack()                            #将三个标签置于窗口内
    frm1.pack(side=TOP)
    frm2.pack()
    #进行分析

    window.mainloop()                    #有这个函数才能看到界面

    import os
    os.remove("show.txt")