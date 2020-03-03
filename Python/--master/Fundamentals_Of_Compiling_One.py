###词法分析###
import sys
from Fundamentals_Of_Compiling_OneOfGui import *
import keyword
def JudgeWord(ch): #判断是否可组成一个字符串
    if ch.isdigit() or ch.isalpha() or ch=='_': return True
    else: return  False
def CreatDict(w,b,t,p):   #创建字典
    return dict(Words=w,BinarySequences=b,Type=t,Point=p)
def I_J(i,j):#下标变化
    if line[j]==' ':i=j+1
    else:i=j
    return i,j
def G_Operator(ch): #关系运算符判断
    GOperator=['<','>','=','<=','>=','<>']
    if ch in GOperator: return True
    else:return False
def S_Operator(ch): #算术运算符判断
    SOperator=['+','-','*','/','%','=']
    if ch in SOperator:return True
    else:return False
def Delimiter(ch): #分界符判断
    d=[',',':',';','(',')','[',']','{','}']
    if ch in d:return True
    else:return False
def ListToStr(l):  #列表转字符串
    s1=[str(i) for i in l]
    return ''.join(s1)
def JudgeError(line,i,l,H,L,d):  #判断出错
    s=''
    if str(line[i]).isdigit():
        l.append(line[i])
        i+=1
        while line[i] == ' ': i += 1  # 清楚空格
        if str(line[i]).isalnum():
            l.append(line[i])
            s=ListToStr(l)
            d=CreatDict(s,('ERROR'),('错误'),(H, L))
            i += 1
    elif S_Operator(line[i]):
        l.append(line[i])
        i+=1
        while line[i]==' ': i+=1
        if Delimiter(line[i]):
            s=ListToStr(l)
            d = CreatDict(s,('ERROR'),('错误'),(H, L))
    return d,i
def ReadStr(line,H,L,i):    #读出一个连续的字符串
    j=i
    l=[]
    d={}
    sign=True
    d,j=JudgeError(line,j,l,H,L,d)
    if d=={}:
        j=i
        l=[]
    else :
        i,j=I_J(i,j)
        return d,i
    while line[j] == ' ': j += 1  # 清楚空格
    if line[j].isalpha() or line[j]=='_': #关键字或者字符串
        while (JudgeWord(line[j])):
            l.append(line[j])
            j+=1
        s=ListToStr(l)
        if keyword.iskeyword(s):
            d=CreatDict(s,(1,s),'关键字',(H,L))
        else:d=CreatDict(s,(6,s),'标识符',(H,L))
    elif line[j].isdigit():   #常数
        while(line[j].isdigit()):
            l.append(line[j])
            j+=1
        s=ListToStr(l)
        if s.isdigit():
            d=CreatDict(s,(5,s),'常数',(H,L))
    elif S_Operator(line[j]): #算术运算符
        while(S_Operator(line[j])):
            l.append(line[j])
            j+=1
        s=ListToStr(l)
        d=CreatDict(s,(3,s),'算术符',(H,L))
    elif G_Operator(line[j]):  #关系运算符
        while (G_Operator(line[j])):
            l.append(line[j])
            j+=1
        s = ListToStr(l)
        d = CreatDict(s, (4, s), '关系符', (H, L))
    elif Delimiter(line[j]):#分界符
        s=ListToStr(line[j])
        j+=1
        d=CreatDict(s,(2,s),'分界符',(H,L))
    elif line[j]=='#':    #注释内容
        j=len(line)
        i=j
        return d,i
    i,j = I_J(i, j)
    return d,i

if __name__=='__main__':
    def makeUpper():   #使用标准流
        f=open('dataTwo.txt','r',encoding='UTF-8')
        lis=f.readline()
        while lis!='':
            print(lis)
            lis=f.readline()
        f.close()
    f = open('dataOne.txt', 'r')
    f1 = open('dataTwo.txt', 'w', encoding='UTF-8')
    line = f.readline()
    H = 1
    l = []
    while line != '':
        L = 1
        i = 0
        while (i < len(line) - 1):
            d, i = ReadStr(line, H, L, i)
            if i == len(line) and d == {}: break
            L += 1
            l.append(d)
        line = f.readline()
        H += 1
    print('%-20s' % 'word', '%-20s' % 'BinarySequences', '%-20s' % 'Type', '%-20s' % 'Location', end='\n', file=f1)
    for d in l:
        print('%-20s' % d['Words'], '%-20s' % str(d['BinarySequences']), '%-20s' % d['Type'],
              '%-20s' % str(d['Point']), end='\n', file=f1)
    f.close()
    f1.close()
    root = Tk()
    Button(root, text='RESULT', command=lambda: redirectionGuiFunc(makeUpper)).pack(fill=X)
    root.title('词法分析器')
    root.mainloop()



