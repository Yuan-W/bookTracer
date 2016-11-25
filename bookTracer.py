#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from bookParser import BookParser
import threading
import glob, os, copy
import json

class TraceThread(threading.Thread):
    def __init__(self, threadID, book):
        threading.Thread.__init__(self)
        self._threadID = threadID
        self._book = book

    def run(self):
        # print "Starting thread %d" % self._threadID
        # print self._book['url']
        self.updateBook()
        # print "Exiting thread %d" % self._threadID

    def getChapters(self, url, getInfo = False):
        parser = BookParser(url)

        chapters = parser.getChapters()
        if getInfo:
            return chapters, parser.getBookInfo()
        return chapters

    def updateBook(self):
        book = self._book
        if 'title' not in book:
            chapters, book['title'] = self.getChapters(book['url'], True)
        else:
            chapters = self.getChapters(book['url'])

        path = 'book'

        if('total_chapters' not in book or len(chapters) != book['total_chapters']):
            lastUpdated = 0 if 'total_chapters' not in book else book['total_chapters']

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
    path = 'book'

    i = 0
    threads = []
    for file in glob.glob("%s/*.json" % path):
        with open(file, 'r') as fp:
            book = json.load(fp)
        thread = TraceThread(i, book)
        thread.start()
        threads.append(thread)
        # updateBook(book)
        i += 1
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()