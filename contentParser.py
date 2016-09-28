#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from bookTracer import findRule
from parser import MyHTMLParser
import codecs

def main():
    file = "book/天工.json"

    with open(file, 'r') as fp:
        book = json.load(fp)

    website = book['url'].split('/')[2]

    rule = findRule(website)

    chapters = book['chapters']

    parser = MyHTMLParser()

    # for chapter in chapters:
    chapter = chapters[-1]
    contents = parser.parseContent(chapter['url'], rule)

    f = codecs.open('%s.txt' % chapter['title'], 'w', "utf-8")
    f.write(contents)
    f.close()

if __name__ == "__main__":
    main()