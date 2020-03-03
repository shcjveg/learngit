#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10
# @Author  : cjshao
# @File    : createParsingTable.py
# @Software: PyCharm


from grammar import Grammar


def firstof(grammar):  # 求解First() 返回每个字符的First组成的列表
    # first & follow sets, epsilon-productions
    firstSet = {i: set() for i in grammar.nonterminals}
    firstSet.update((i, {i}) for i in grammar.terminals)
    epsilon = set()

    while True:
        updated = False

        for nt, expression in grammar.rules:
            # FIRST set w.r.t epsilon-productions
            for symbol in expression:
                updated |= union(firstSet[nt], firstSet[symbol])
                if symbol not in epsilon:
                    break
            else:
                updated |= union(epsilon, {nt})

        if not updated:
            return firstSet


def union(first, begins):
    n = len(first)
    first |= begins
    return len(first) != n


def checkValidity(i):
    if i[0][-1] == '.':
        print('*************')
        return False
    return True


def preProcessStates(states):
    """
    由于follow字符和产生式之间没有分隔，所以做闭包时会有把follow字符也考虑进去的情况，此函数用于避免这种情况也被加入状态
    （以防万一，事实上在GOTO()中已做条件约束，一般情况下不会调用该函数）
    """
    l = []
    for i in states:
        if checkValidity(i):
            l.append(''.join(i).replace(' ', ''))

    if len(l) != 0:
        return (l)


def is_nonterminal(symbol):
    return symbol.isupper()


def shiftPos(item):  # 向后平移.
    Item = ''.join(item).replace(' ', '')
    listItem = list(Item)
    index = listItem.index('.')
    if len(listItem[index:]) != 1:
        return (Item[:index] + '' + Item[index + 1] + '.' + Item[index + 2:])
    return item


def check(item, N):
    """
    Input:['A::=B.b$'],b
    Output:True

    判断是否是对应转化条件且符合.的位置的产生式
    """
    Item = ''.join(item).replace(' ', '')
    listItem = list(Item)
    try:
        index = listItem.index('.')
        # index1=listItem.index('=')
        if N == listItem[index + 1]:
            return True
        if ' ' == listItem[index + 1]:
            return False
    except:
        return False


def GOTO(I, N, first, entryOfGram):
    """
    Input: ['S::=.CC$'],C
    Output: [['S::=C.C$'], ['C::=.cC$'], ['C::=.d$']]

    对符合GOTO转化条件的产生式做.的向后移动并返回做闭包的产生式组
    """
    J = []
    for i in I:
        if isinstance(i, list):
            temp = i[0]
        else:
            temp = i
        if check(i, N) and temp[-2] != '.':
            new = shiftPos(i)
            J.append(new)

    if len(J) == 0:
        return ([])

    return (findClosure([J], first, entryOfGram))


def allGrammarSymbol(item):
    """
    Input: item
    Output: Grammar Symbols

    文法中所有符号
    """
    l = []
    # print(type(item))
    for i in item.values():
        for k in ''.join(i):
            # if k.isalpha():
            # print(k)
            if k != '$':
                l.append(k)

    return set(l)


def findProduction(B, entryOfGram):
    """
    Input : 'S'
    Output: ['CC']

    寻找B的产生式
    """

    if B == '$':
        return None
    if B not in entryOfGram.keys():
        return None
    return entryOfGram[B]


def findTerminalsOf(gram):
    newList = {}
    for i in gram:
        n = i.replace(' ', '').split('::=')
        if n[0] not in newList.keys():
            newList[n[0]] = [''.join(n[1])]
        else:
            newList[n[0]].append(''.join(n[1]))
    return newList


def nextDotPos(item):
    """
    input:'A::=.A$'
    output :'A'

    输出.后的符号
    """
    Item = item.replace(' ', '')
    listItem = list(Item)
    try:
        index = listItem.index('.')
        return listItem[index + 1]
    except:
        return '$'


def followOf(item):
    """
    input:'A::.AB'
    output: 'B'

    返回.后的第二个符号（向后看一位），也就是follow符号
    """
    Item = item.replace(' ', '')
    listItem = list(Item)
    try:
        index = listItem.index('.')
        return listItem[index + 2]
    except IndexError:
        return '$'


def findClosure(I, first, entryOfGram):
    """
    Input: '^::=.S$''
    Output : [['^::=.S$'], ['S::=.CC$'], ['C::=.cCd'], ['C::=.cCc'], ['C::=.dd'], ['C::=.dc']]

    求闭包并在每个产生式末尾添加follow符号
    """
    add = 1
    while (add != 0):
        add = 0
        for item in I:
            for i in item:
                element = i
                giveElement = nextDotPos(element)  # 返回.后符号
                findPr = findProduction(giveElement, entryOfGram)  # 寻找giveElement的产生式
                if findPr == None:  # 没有对应的产生式右部
                    pass
                else:  # 有则遍历所有giveElement的产生式右部
                    for productions in findPr:
                        try:
                            for b in first[followOf(element)]:
                                elem = [giveElement + '::=.' + productions + b]  # 向后看一位，即：LR(1)
                                if elem not in I:
                                    I.append(elem)
                                    add = 1
                        except:
                            print("Error: 传入文法有误，请检查是否在首行后加$")

        return (I)
        break


def createtable(gram, first):  # 返回LR(1)parsingTable字典列表
    ACTION = []
    start0 = gram[0]
    # print(list(start0).index('=')+1)
    list0 = list(start0)
    list0.insert((list(start0).index('=') + 1), '.')
    # print(list0)
    starting = ''.join(list0)
    # print(starting)

    entryOfGram = findTerminalsOf(gram)  # 将文法字典化
    print('文法字典化', entryOfGram)

    I = [findClosure([[starting]], first, entryOfGram)]  # 找到初始状态I0的全部产生式（闭包）
    # findClosure(GOTO(I[0],'d'))

    X = allGrammarSymbol(entryOfGram)  # 返回文法中所有符号
    print('返回文法中所有转移符号', X)

    allItems = {}
    ItemsAll = []
    new_item = True
    while new_item:
        new_item = False
        i = 1
        for item in I:
            i += 1
            for g in X:
                if len(GOTO(item, g, first, entryOfGram)) != 0:
                    goto = GOTO(item, g, first, entryOfGram)  # 返回状态转移后的新状态的产生式（闭包）组
                    flat_list = [[item] for sublist in goto for item in sublist]
                    if flat_list not in I:
                        index = 'I' + str(i)
                        if index not in allItems.keys():
                            allItems[index] = [g]
                        else:
                            allItems[index].append(g)
                        I.append(flat_list)
                        Z = preProcessStates(flat_list)
                        if (Z):
                            ItemsAll.append(flat_list)
                            # index = ItemsAll.index(flat_list)
                            # # ACTION[str(i - 1) + '+' + gotoElem] = "shift " + str(index)
                            # if len(ACTION) < i:
                            #     ACTION.append({g: "shift " + str(index+1)})
                            # elif g not in ACTION[i - 1].keys():
                            #     ACTION[i - 1][g] = "shift " + str(index+1)
                            # else:
                            #     print("发现冲突!")
                            #     print(ACTION[i - 1][g])
                            #     print("shift " + str(index+1))

                        new_item = True

        new_item = False

    ItemsAll.insert(0, findClosure([[starting]], first, entryOfGram))
    i = 0
    # ACTION = {}

    # print(ItemsAll)
    print('--------------------------------')
    for item in ItemsAll:
        i += 1
        for num in item:
            x = list(num[0]).index('.') + 2
            y = len(num[0])
            if x < y:
                elem = list(num[0]).index('.') + 1
                gotoElem = list(num[0])[elem]
                # IJ = GOTO(num, gotoElem, first, entryOfGram)
                goto = GOTO(item, gotoElem, first, entryOfGram)
                # print(IJ)
                IJ = [[item] for sublist in goto for item in sublist]
                if IJ in ItemsAll:
                    # print('aa')
                    # print(num)
                    index = ItemsAll.index(IJ)
                    last = list(num[0])[len(num[0]) - 1]
                    # ACTION[str(i - 1) + '+' + gotoElem] = "shift " + str(index)
                    temp = "shift " + str(index)
                    if len(ACTION) < i:
                        ACTION.append({gotoElem: temp})
                    elif gotoElem not in ACTION[i - 1].keys():
                        ACTION[i - 1][gotoElem] = temp
                    elif ACTION[i - 1][gotoElem] != temp:
                        print("发现冲突: ", i - 1)
                        print(ACTION[i - 1][gotoElem])
                        print(temp)
            else:
                listy = list(num[0]).index('.')
                el = num[0][listy + 1]
                # ACTION[str(i - 1) + '+' + el] = "reduce " + num[0][:listy]
                if len(ACTION) < i:
                    if num[0][:listy]+'$' != gram[0]:
                        ACTION.append({el: "reduce " + num[0][:listy]})
                    else:
                        ACTION.append({el: 'ACC'})

                elif el not in ACTION[i - 1].keys():
                    if num[0][:listy]+'$' != gram[0]:
                        ACTION[i - 1][el] = "reduce " + num[0][:listy]
                    else:
                        ACTION[i - 1][el] = 'ACC'

                else:
                    print("发现冲突: ", i - 1)
                    print(ACTION[i - 1][el])
                    # ACTION[i-1].update({el: "reduce" + num[0]})
                    print("reduce " + num[0][:listy])

        # print(num[0])

    # print(ACTION)
    print('--------------------------------')

    print('**** LR(1) DFA ****')
    for i in ItemsAll:
        print('I' + str(ItemsAll.index(i)))
        print(i)
        print('--------------------------------')

    # print(ItemsAll)
    return ACTION
