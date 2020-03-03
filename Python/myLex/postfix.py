# -*- coding: utf-8 -*-
# @Time    : 2019/12/4
# @Author  : cjshao
# @File    : postfix.py
# @Software: PyCharm

word = 'abcdefghijklmnopqrstuvwxyz'


def addsymbol(str):  # 正规式重写
    addstr = str
    before_add = 0  # 已经插入的+号数量，用于切割字符串时进行后移
    str_len = len(str)
    for i in range(str_len):
        if str[i] in word:
            if i < (str_len - 1):
                if str[i + 1] in word:
                    addstr = addstr[:i + before_add + 1] + '.' + addstr[i + before_add + 1:]
                    before_add = before_add + 1
                elif str[i + 1] == '*' and i < (str_len - 2):
                    if str[i + 2] in word:
                        addstr = addstr[:i + before_add + 2] + '.' + addstr[i + before_add + 2:]
                        before_add = before_add + 1
                elif str[i + 1] == '(':
                    addstr = addstr[:i + before_add + 1] + '.' + addstr[i + before_add + 1:]
                    before_add = before_add + 1
        if i < (str_len - 1) and (str[i] == '*' and str[i+1] == '(') or (str[i] == ')' and str[i+1] == '(') or \
                (str[i] == ')' and str[i+1] in word):
            addstr = addstr[:i + before_add + 1] + '.' + addstr[i + before_add + 1:]
            before_add = before_add + 1
    return addstr


def reserve(str):  # 正则式转后缀式
    str = addsymbol(str)
    print('将连接规则添加进正规式，重写之后为：', str)
    in_stack = {'.': 2, '|': 1, '(': 0, ')': 0, '*': 0}
    out_stack = {'.': 2, '|': 1, '(': 3, ')': 10, '*': 11}
    result = []  # 结果集
    stack = []  # 符号栈
    addFlag = 0  # 判断+号是否出栈
    for i in str:
        if i in word or i == '*':  # 1.是字母直接压入结果集 2. 是*直接压入结果集
            result.append(i)
        elif i in '|().':
            # if i == '+':
            #     addFlag = 1   #说明栈中有+
            if len(stack) == 0:  # 如果栈为空直接压入
                stack.append(i)
            else:  # 栈不为空时
                top_char = stack[len(stack) - 1]  # 获取栈顶元素
                if i == '(':  # 为左括号直接压入
                    if addFlag > 0 and stack[len(stack) - 1] == '.':
                        addSymbol = stack.pop()
                        result.append(addSymbol)
                        addFlag = 0
                    stack.append(i)
                elif i == ')':  # 为右括号时
                    if '.' in stack:
                        addFlag = addFlag + 1
                    catch_pop_char = ''
                    while len(stack) != 0:  # 一直弹出直到左括号
                        catch_pop_char = stack.pop()
                        if catch_pop_char == '(':
                            # if len(stack) != 0 and stack[len(stack) - 1] == '+':
                            #     addSymbol = stack.pop()
                            #     result.append(addSymbol)
                            break
                        else:
                            result.append(catch_pop_char)
                            if catch_pop_char == ".":
                                addFlag = addFlag - 1
                else:
                    top = stack[len(stack) - 1]  # 获得栈顶
                    if out_stack[i] > in_stack[top]:  # 栈外大，栈内小，直接压入
                        stack.append(i)
                    else:  # 栈外小，栈内大，弹出直到栈空或者栈外大
                        catch = stack.pop()
                        result.append(catch)
                        if catch == "." and addFlag > 0:
                            addFlag = addFlag - 1
                        while len(stack) != 0:
                            top = stack[len(stack) - 1]
                            if out_stack[i] > in_stack[top]:
                                # stack.append(i)
                                break
                            else:
                                catch = stack.pop()
                                result.append(catch)
                                if catch == "." and addFlag > 0:
                                    addFlag = addFlag - 1
                        stack.append(i)
        else:
            print('你输入的正则表达式有问题哦')
    while len(stack) != 0:
        catch_pop_char = stack.pop()
        result.append(catch_pop_char)
    result_str = ''
    print('result:', result)
    for i in result:
        result_str = result_str + i

    return result_str


if __name__ == '__main__':
    # 正规式重写测试
    #str = '(ab)*(a|b)*(abc)'
    str = '(a*b)*(a|b)'
    # str = push_some_add(str)
    # print(str)
    str = reserve(str)  # 正则式转后缀式

    print(str)
