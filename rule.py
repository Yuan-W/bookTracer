#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parser_base import Parser
import glob, os
import json

class BookRule():
    def __init__(self, fileName):
        self.__file = fileName
        with open(fileName, 'r') as fp:
            self.__rules = json.load(fp)

    def __update(self, rule):
        for r in self.__rules:
            if r['website'] == rule['website']:
                r = rule
        with open(self.__file, 'w') as fp:
            json.dump(rules, fp)

    def find(self, website):
        if(website.startswith('http://')):
            website = website.split('/')[2]
        rule = (r for r in self.__rules if r['website'] == website).next()
        if('charset' not in rule):
            url = 'http://%s' % rule['website']
            rule['charset'] = Parser(url).getCharset()
            self._update(rule)
        return rule