#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/4
# @Author  : cjshao
# @File    : main.py
# @Software: PyCharm

from creatDFAo import *
import postfix
import re


# 1.读取正规表达式文件，每个生成一个NFA
# 2.用or_two_Node()方法连接多个NFA
# 3.由NFA生成DFAo
# 4.扫描源程序文件，以空格为分隔逐个读取字段
# 5.1 判断字段是否为保留字、符号，是则打印TOKEN；否则进入5.2
# 5.2 根据生成的DFAo进行识别：整形常数（常量）；标识符；识别出错。不出错则打印TOKEN，出错则停止程序，打印错误信息。


def oneNFA(re):  # 由单个正规表达式生成一个子NFA
    wordlist = getWord(re)
    strTest = postfix.reserve(re)
    NFA = createNFA(strTest, wordlist)
    return NFA


def mergeNFA(NFA0, re):  # 合并NFA
    wordlist = getWord(re)
    # print(re)
    strTest = postfix.reserve(re)
    NFA = createNFA(strTest, wordlist)
    newLink = OperateLink('_')
    newLink.or_two_Node(NFA0, NFA)
    return newLink


def DFAopt(NFA, wordDic):  # 生成DFAo
    NFA.getfirstNode().isFirst = True
    queue = []  # NFA状态队列
    print_to_queue(NFA.getfirstNode(), queue)
    # NFA_relation(queue)  # 打印NFA
    set_isend_inNFA(queue)  # 标识终态

    # 初态
    state = set()  # 存放初始状态
    getbegin(NFA.getfirstNode(), state)

    # 通过初始状态生成DFA（没有化简的版本）#
    statelist = [state]  # 初始的生成DFA只有一个状态
    DFA = getDFA(queue, statelist, wordDic)  # 获得DFA
    DFAo = optDFA(statelist, queue, DFA, wordDic)

    return DFAo


keyWords = {'False': 101, 'class': 102, 'finally': 103, 'is': 104, 'return': 105, 'None': 106, 'continue': 107,
            'for': 108, 'lambda': 109, 'try': 110, 'True': 111, 'def': 112, 'from': 113, 'nonlocal': 114, 'while': 115,
            'and': 116, 'del': 117, 'global': 118, 'not': 119, 'with': 120, 'as': 121, 'elif': 122, 'if': 123,
            'or': 124, 'yield': 125, 'assert': 126, 'else': 127, 'import': 128, 'pass': 129, 'break': 130,
            'except': 131, 'in': 132, 'raise': 133, '+': 201, '-': 202, '*': 203, '/': 204, '=': 205, ':': 206,
            '<': 207, '>': 208, '%': 209, '&': 210, '!': 211, '(': 212, ')': 213, '[': 214, ']': 215, '{': 216,
            '}': 217, '#': 218, '|': 219, ',': 220}


def isKeyWord(item, keyWords, f):  # 判断是否为指定的保留字或符号，若是则写入
    if item in keyWords.keys():
        if keyWords[item] < 201:
            writeToken(('RESERVED', item.upper(), str(keyWords[item])), f)
            # f.write('\n')
        else:
            writeToken(('SYMBOL', item, str(keyWords[item])), f)
            # f.write('\n')
        return True
    else:
        return False


def DFAmoniter(DFAo, symbol, stateIndex):  # 读取DFA进行判断
    stateIndex = DFAo[stateIndex][symbol]
    return stateIndex


def isIdentifier(item, f, DFAo):  # 标识符及常量NUM识别
    itemList = item.strip('')
    # if re.match(r'[A-Za-z_]', itemList[0]):
    stateIndex = 0
    count = 0
    itemType = -1
    for i in itemList:
        count += 1
        if re.match(r'[0-9]', i):
            if count == 1:
                itemType = 0  # 数字
            stateIndex = DFAmoniter(DFAo, 'd', stateIndex)
        elif re.match(r'[A-Za-z_]', i):
            if count == 1:
                itemType = 1  # 字母
            stateIndex = DFAmoniter(DFAo, 'l', stateIndex)
        else:
            print('匹配失败')
            return False
        if stateIndex == None:
            print('匹配失败')
            return False
    # writeToken(('IDENTIFIER', item, str(keyWords[item])), f)
    # f.write('\n')
    if itemType == 1:
        f.write('<IDENTIFIER: ' + item + '>\n')
    elif itemType == 0:
        f.write('<NUM: ' + item + '>\n')
    else:
        print('Error!')
    return True


def writeToken(item, f):  # 写token到文件中(main中打开)
    # with open('out.txt', 'a') as f:
    token = '<' + item[0] + ',' + item[1] + ',' + item[2] + '>\n'
    f.write(token)


if __name__ == '__main__':
    # strTest1 = 'dd*'
    # strTest2 = 'l(l|d)*'
    # ==========生成REs.txt中全部正规表达式连接的DFAo==========#
    wordDic = set()  # 存放正规表达式的字母
    try:
        with open('REs.txt') as reFile:
            reLines = reFile.readlines()
            print(reLines)
            reTemp = reLines.pop().strip('\n')
            print("读取的正规表达式为: ", reTemp)
            NFATemp = oneNFA(reTemp)
            wordDic.update(getWord(reTemp))
            # print(wordDic)
            while len(reLines) > 0:
                reTemp = reLines.pop().strip('\n')
                # print(reTemp)
                wordDic.update(getWord(reTemp))
                # print(wordDic)
                NFATemp = mergeNFA(NFATemp, reTemp)
    except IOError:
        print('Error: 没有找到RES.txt文件或读取文件失败', IOError)
    DFAo = DFAopt(NFATemp, wordDic)
    # print(DFAo)
    # ==========扫描源程序文件，以空格(可以是多个空格)为分隔逐个读取字段==========#
    try:
        with open('program.txt') as pFile:
            words = pFile.readlines()  # .strip('\n').split(' ')
            symbols = []
            for line in words:
                symbols.extend(line.strip('\n').split(' '))
            while '' in symbols:
                symbols.remove('')
            print(symbols)
    except IOError:
        print('Error: 没有找到program.txt文件或读取文件失败', IOError)
    # ==========判断字段是否为保留字、符号==========#
    # 是则打印TOKEN，否则进入标识符判断
    try:
        with open('out.txt', 'a') as f:
            f.seek(0)
            f.truncate()
            for item in symbols:
                if(isKeyWord(item, keyWords, f) == False):
                    # ==========标识符判断==========#
                    # 根据生成的DFAo进行识别：整形常数（常量）；标识符；识别出错。不出错则打印TOKEN，出错则停止程序，打印错误信息
                    if (isIdentifier(item, f, DFAo) == False):
                        print('Error: 检测出错--->', item)
                        break
    except IOError:
        print('Error: 没有找到out.txt文件或写入文件失败', IOError)

