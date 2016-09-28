#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from parser import MyHTMLParser
import glob, os
import json

# from pg import DB

def findRule(website):
    with open('rules.json', 'r') as fp:
        rules = json.load(fp)

    return (rule for rule in rules if rule['website'] == website).next()

def updateRule():
    parser = MyHTMLParser()
    with open('rules.json', 'r') as fp:
        rules = json.load(fp)

    for rule in rules:
        if('charset' not in rule):
            url = 'http://%s' % rule['website']
            rule['charset'] = parser.detectCharset(url)
            print rule
    with open('rules.json', 'w') as fp:
        json.dump(rules, fp)

def getChapters(book, depthLimit=1):
    parser = MyHTMLParser()

    website = book['url'].split('/')[2]

    rule = findRule(website)

    chapters = parser.parseChapters(book, rule)

    return chapters

def updateBook(book):
    chapters = getChapters(book, 1)

    path = 'test' if test else 'book'

    if('total_chapters' not in book or len(chapters) != book['total_chapters']):
        lastUpdated = book['total_chapters']
        book['total_chapters'] = len(chapters)
        book['chapters'] = chapters

        fileName = '%s/%s.json' % (path, book['title'])
        with open(fileName, 'w') as fp:
            json.dump(book, fp)
        print('%s updated' % book['title'])
        for i in range(lastUpdated, len(chapters)):
            print(chapters[i]['title'])
    else:
        print('No update for %s' % book['title'])

def main():
    updateRule()

    path = 'test' if test else 'book'

    print path

    for file in glob.glob("%s/*.json" % path):
        with open(file, 'r') as fp:
            book = json.load(fp)
        updateBook(book)

if __name__ == "__main__":
    test = True
    main()