''''

Find Closure and Contents of a CLR Parsing Table

input>>
    '^::=S$',
    'S::=CC',
    'C::=cC',
    'C::=d'

Output>>
    {'0+S': 'shift 2', '0+C': 'shift 3', '0+c': 'shift 10', '0+d': 'shift 8',
     '1+d': 'reduce C::=d', '1+c': 'reduce C::=d', '2+$': 'reduce ^::=S', '3+C': 'shift 6',
     '3+c': 'shift 7', '3+d': 'shift 5', '4+C': 'shift 12', '4+c': 'shift 10', '4+d': 'shift 8',
    '5+$': 'reduce C::=d', '6+$': 'reduce S::=CC', '7+C': 'shift 11', '7+c': 'shift 7',
    '7+d': 'shift 5', '8+d': 'reduce C::=d', '9+d': 'reduce C::=cC', '9+c': 'reduce C::=cC',
    '10+C': 'shift 12', '10+c': 'shift 10', '10+d': 'shift 8', '11+$': 'reduce C::=cC', '12+d': 'reduce C::=cC'}
    (Contents Of Parsing Table)
    where an entry,
    5+$: 'reduce C::=d' represents reduction in state 5 , under $ symbol from d to C.


    State  0
    [['^::=.S$'], ['S::=.CC$'], ['C::=.cCd'], ['C::=.cCc'], ['C::=.dd'], ['C::=.dc']]
    *********************
    State  1
    [['C::=d.d'], ['C::=d.c']]
    *********************
    State  2
    [['^::=S.$']]
    *********************
    State  3
    [['S::=C.C$'], ['C::=.cC$'], ['C::=.d$']]
    *********************
    State  4
    [['C::=c.Cd'], ['C::=c.Cc'], ['C::=.cCd'], ['C::=.dd']]
    *********************
    State  5
    [['C::=d.$']]
    *********************
    State  6
    [['S::=CC.$']]
    *********************
    State  7
    [['C::=c.C$'], ['C::=.cC$'], ['C::=.d$']]
    *********************
    State  8
    [['C::=d.d']]
    *********************
    State  9
    [['C::=cC.d'], ['C::=cC.c']]
    *********************
    State  10
    [['C::=c.Cd'], ['C::=.cCd'], ['C::=.dd']]
    *********************
    State  11
    [['C::=cC.$']]
    *********************
    State  12
    [['C::=cC.d']]
    *********************


    All Possible States





'''

from first import first, grammar


def checkValidity(i):
    if i[0][-1] == '.':
        return False
    return True


def preProcessStates(states):
    '''
    One of the implementation error:
    Since our grammar is in the form 'A::=Bb' where b is the follow of the grammar.

    The program could not distinguish the follow element from the other elements, hence, we need this function to
    avoid that.

    由于follow字符和产生式之间没有分隔，所以做闭包时会有把follow字符也考虑进去的情况，此函数用于避免这种情况也被加入状态

    '''
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
    '''
    Check if the grammar is not completely parsed or not
    Input: Item, GrammarSymbol
    Output: True if . can be shifted else False

    Example1:
    Input:['A::=B.b$'],b
    Output:True

    判断是否是对应转化条件且符合.的位置的产生式
    '''
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


def GOTO(I, N):
    '''
    Input: (Item,GrammarSymbol)
    Output: Closure of Item after shift grammar GrammarSymbol is performed

    Example:
    Input: ['S::=.CC$'],C
    Output: [['S::=C.C$'], ['C::=.cC$'], ['C::=.d$']]

    对符合GOTO转化条件的产生式做.的向后移动
    '''
    J = []
    for i in I:
        if check(i, N):
            new = shiftPos(i)
            J.append(new)

    if len(J) == 0:
        return ([])

    return (findClosure([J]))


def allGrammarSymbol(item):
    '''
    Input: All sets of Grammar(our main input)
    Output: Grammar Symbols
    '''
    l = []
    for i in item:
        for k in i:
            if k.isalpha():
                l.append(k)

    return set(l)


def findProduction(B):
    '''
    Input: A non-terminal B
    Output: All Productions of B
    Example
    Input : 'S'
    Output: ['CC']

    寻找B的产生式
    '''

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
    '''
    input: An item
    output: The element to be executed

    Example
    input:'A::=.A$'
    output :'A'

    输出.后的符号
    '''
    Item = item.replace(' ', '')
    listItem = list(Item)
    try:
        index = listItem.index('.')
        return listItem[index + 1]
    except:
        return '$'


def followOf(item):
    '''
    input: An item
    output: The next non-terminal to be opened up

    Example
    input:'A::.AB'
    output: 'B'

    返回.后的第二个符号（向后看一位），也就是follow符号
    '''
    Item = item.replace(' ', '')
    listItem = list(Item)
    try:
        index = listItem.index('.')
        return listItem[index + 2]
    except IndexError:
        return '$'


def findClosure(I):
    '''
    Input: Grammar I
    Output : Closure of Grammar

    Input: '^::=.S$''
    Output : [['^::=.S$'], ['S::=.CC$'], ['C::=.cCd'], ['C::=.cCc'], ['C::=.dd'], ['C::=.dc']]

    where last element is the follow element.
    Example:
    In ['^::=.S$'] , $ is the follow of '^::=.S'

    在每个产生式末尾添加follow
    '''
    add = 1
    while (add != 0):
        add = 0
        for item in I:
            element = item[0]
            giveElement = nextDotPos(element)  # 返回.后符号
            findPr = findProduction(giveElement)  # 寻找giveElement的产生式
            if findPr == None:  # 没有对应的产生式右部
                pass
            else:  # 有则遍历所有giveElement的产生式右部
                for productions in findPr:
                    for b in first[followOf(element)]:
                        elem = [giveElement + '::=.' + productions + b]  # 向后看一位，即：LR(1)
                        if elem not in I:
                            I.append(elem)
                            add = 1
        return (I)
        break


# gram = (
#     '^::=S$',
#     'S::=CC',
#     'C::=cC',
#     'C::=d'
# )
# starting = '^::=.S$'

# gram = (
#     'S::=E$',
#     'E::=E+T',
#     'E::=T',
#     'T::=T*F',
#     'T::=F',
#     'F::=(E)',
#     'F::=d'
# )
# starting = 'S::=E$'
# You can update your Grammar here. Be sure you update it on first.py line no. 61 as well.
# Also add the augmented Grammar like in line 269
# Adjust line 278 acc. to your need

gram = grammar
start0 = gram[0]
# print(list(start0).index('=')+1)
list0 = list(start0)
list0.insert((list(start0).index('=')+1), '.')
# print(list0)
starting = ''.join(list0)
# print(starting)


entryOfGram = findTerminalsOf(gram)  # 将文法字典化
I = [findClosure([[starting]])]  # 找到初始状态I0的全部产生式（闭包）
# findClosure(GOTO(I[0],'d'))

X = allGrammarSymbol(gram)  # 返回文法中所有字母符号

allItems = {}
ItemsAll = []
new_item = True
while new_item:
    new_item = False
    i = 1
    for item in I:
        i += 1
        for g in X:
            if len(GOTO(item, g)) != 0:
                goto = GOTO(item, g)  # 返回状态转移后的新状态的产生式（闭包）组
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

                    new_item = True

    new_item = False

ItemsAll.insert(0, findClosure([[starting]]))
i = 0
# ACTION = {}
ACTION = []
# print(ItemsAll)
print('*********************')
for item in ItemsAll:
    i += 1
    for num in item:
        x = list(num[0]).index('.') + 2
        y = len(num[0])
        if x < y:
            elem = list(num[0]).index('.') + 1
            gotoElem = list(num[0])[elem]
            IJ = GOTO(num, gotoElem)
            # print(IJ)
            if IJ in ItemsAll:
                # print('aa')
                # print(num)
                index = ItemsAll.index(IJ)
                last = list(num[0])[len(num[0]) - 1]
                # ACTION[str(i - 1) + '+' + gotoElem] = "shift " + str(index)
                if len(ACTION) < i:
                    ACTION.append({gotoElem : "shift " + str(index)})
                elif gotoElem not in ACTION[i-1].keys():
                    ACTION[i-1][gotoElem] = "shift " + str(index)
                else:
                    print("发现冲突!")
                    print(ACTION[i-1][gotoElem])
                    print("shift " + str(index))
        else:
            listy = list(num[0]).index('.')
            el = num[0][listy + 1]
            # ACTION[str(i - 1) + '+' + el] = "reduce " + num[0][:listy]
            if len(ACTION) < i:
                ACTION.append({el: "reduce " + num[0][:listy]})
            elif el not in ACTION[i - 1].keys():
                ACTION[i - 1][el] = "reduce " + num[0][:listy]
            else:
                print("发现冲突!")
                print(ACTION[i - 1][el])
                print("reduce " + num[0][:listy])

    # print(num[0])

print(ACTION)
print('*************************')

print('**** All States Are ****')
for i in ItemsAll:
    print('State ', ItemsAll.index(i))
    print(i)
    print('*********************')
