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

def getChapters(book, depthLimit=1):
    parser = HTMLParser()

    website = book['url'].split('/')[2]

    rule = findRule(website)

    chapters = parser.parseChapters(book, rule)

    return chapters

def updateBook(book):
    chapters = getChapters(book, 1)

    if('total_chapters' not in book or len(chapters) != book['total_chapters']):
        book['total_chapters'] = len(chapters)
        book['chapters'] = chapters
        fileName = 'book/' + book['title']+'.json'
        with open(fileName, 'w') as fp:
            json.dump(book, fp)
        print('%s updated' % book['title'])
    else:
        print('No update for %s' % book['title'])

def main():
    for file in glob.glob("book/*.json"):
        with open(file, 'r') as fp:
            book = json.load(fp)
        updateBook(book)

if __name__ == "__main__":
    main()