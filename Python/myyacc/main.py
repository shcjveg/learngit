#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10
# @Author  : cjshao
# @File    : main.py
# @Software: PyCharm

from createParsingTable import *
import pandas as pd
import re


def monitor(ACTION, inputQueue, f):  # 识别分析表
    """
    Input: LR(1)分析表, 字符串
    Output: 移进规约序列
    """
    # inputQueue = list(string)
    inputQueue.append('$')

    # 开始状态
    stateStack = [0]  # State:Symbol
    symbolStack = ['_']
    while True:
        try:
            readyToOut = inputQueue[0]  # 试探：还未出队
            topState = stateStack[-1]
            topSymbol = symbolStack[-1]
            option = ACTION[topState][readyToOut]
        except:
            # f.write('Syntax Error: ', readyToOut)
            f.write('Syntax Error: ' + str(readyToOut))
            print('中止：不符合语法规则，匹配失败!')
            break

        f.write(
            '-------------------------------------------------------------------------------------------------------------------\n')
        f.write('state: ' + str(stateStack) + '\n')
        f.write('stack: ' + str(symbolStack).ljust(30) + '\t' + 'inputQueue: ' + str(inputQueue).ljust(
            40) + '\t' + 'option: ' + option + '\n')

        print(
            '-------------------------------------------------------------------------------------------------------------------')
        print('state: ' + str(stateStack))
        print('stack: ' + str(symbolStack).ljust(30) + '\t' + 'inputQueue: ' + str(inputQueue).ljust(30), end='\t')
        print('option: ' + option)

        if re.match(r'shift', option):
            guide = re.search(r'(\d+)', option)
            stateStack.append(int(guide.group(1)))
            symbolStack.append(readyToOut)
            inputQueue.pop(0)
        elif re.match(r'reduce', option):
            guide = re.search(r'(\D)::=(\D+)', option)
            for i in range(len(guide.group(2))):
                stateStack.pop()
                symbolStack.pop()
            inputQueue.insert(0, guide.group(1))
        elif re.match(r'ACC', option):
            print(
                '-------------------------------------------------------------------------------------------------------------------')
            f.write(
                '-------------------------------------------------------------------------------------------------------------------\n')
            f.write('符合语法规则，匹配成功！\n\n')
            print('符合语法规则，匹配成功!')
            break
        else:
            f.write(
                '-------------------------------------------------------------------------------------------------------------------\n')
            f.write('不符合语法规则，匹配失败！\n\n')
            print('不符合语法规则，匹配失败orz')
            break


if __name__ == '__main__':
    # first = firstof(Grammar(
    #     'S::=E$',
    #     'E::=E+T',
    #     'E::=T',
    #     'T::=T*F',
    #     'T::=F',
    #     'F::=(E)',
    #     'F::=d'
    # )
    # )
    try:
        with open('CFGs.txt') as cFile:
        # with open('CFG4.7p112.txt') as cFile:
        # with open('CFG4.7p112.txt') as cFile:
            # cLines = cFile.readlines()
            grammar = list(i.strip('\n') for i in cFile.readlines())
            s0 = '^::=' + list(grammar[0])[0] + '$'
            grammar.insert(0, s0)
            grammar = tuple(grammar)
            # print(cLines)
            first = firstof(Grammar(grammar))  # first表
            # print(first)
    except IOError:
        print('Error: 没有找到CFGs.txt文件或读取文件失败', IOError)
    ACTION = createtable(grammar, first)
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    # pd.set_option('display.height', 1000)
    # pd.set_option('display.max_rows', 500)
    # pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    # string = 'd+d*d+d'
    print(pd.DataFrame(ACTION))
    try:
        with open('Strings.txt') as sFile:
        # with open('illegalStrings.txt') as sFile:
            strings = list(i.strip('\n') for i in sFile.readlines())
    except IOError:
        print('Error: 没有找到Strings.txt文件或读取文件失败', IOError)

    # print(strings)
    try:
        with open('out.txt', 'a') as f:
            f.seek(0)
            f.truncate()
            for string in strings:
                print('******************')
                print('Input: ', string)
                f.write('Input: ' + str(string) + '\n')

                strSpl = re.split(r'([+ *])', string)
                for i in range(len(strSpl)):
                    if strSpl[i].isalnum():
                        strSpl[i] = 'd'
                print(''.join(strSpl))
                print('******************')
                monitor(ACTION, strSpl, f)
    except IOError:
        print('Error: 没有找到out.txt文件或写入文件失败', IOError)
