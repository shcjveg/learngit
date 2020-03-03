#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/10
# @Author  : cjshao
# @File    : grammar.py.py
# @Software: PyCharm


class Grammar:

    def __init__(self, rules):
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('::='))

    def __getitem__(self, nonterminal):
        yield from [rule for rule in self.rules
                    if rule[0] == nonterminal]

    @staticmethod
    def is_nonterminal(symbol):
        return symbol.isalpha() and symbol.isupper()

    @property
    def nonterminals(self):
        return set(nt for nt, _ in self.rules)

    @property
    def terminals(self):
        return set(
            symbol
            for _, expression in self.rules
            for symbol in expression
            if not self.is_nonterminal(symbol)
        )