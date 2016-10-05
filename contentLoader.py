#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import threading
import os, glob
from contentParser import ContentParser
import codecs

class DownladThread(threading.Thread):
    def __init__(self, threadID, url, file):
        threading.Thread.__init__(self)
        self._threadID = threadID
        self._url = url
        self._file = file

    def run(self):
        print "Starting thread %d" % self._threadID
        # print self._file, self._url
        parser = ContentParser(self._url)
        content = parser.getContent()
        f = codecs.open(self._file, 'w', "utf-8")
        f.write(content)
        f.close()
        print "Exiting thread %d" % self._threadID

def mergeChapters(title):
    book_file = os.path.join('book', '%s.json' % title)
    with open(book_file, 'r') as fp:
        book = json.load(fp)
    with open('%s.txt' % title, 'w') as outfile:
        outfile.write('%s\r\n' % title)
        for chapter in book['chapters']:
            content_file = os.path.join(title, '%s.txt' % chapter['title'].encode('utf-8'))
            with open(content_file) as infile:
                outfile.write('\r\n')
                outfile.write(chapter['title'].encode('utf-8'))
                outfile.write('\r\n')
                outfile.write(infile.read())

def main():
    path = 'book'

    # file = os.path.join('book', '%s.json' % title)

    for file in glob.glob("%s/*.json" % path):
        title_ext = os.path.basename(file)
        title = os.path.splitext(title_ext)[0]
        if not os.path.isdir(title):
            os.mkdir(title)

        with open(file, 'r') as fp:
            book = json.load(fp)

        website = book['url'].split('/')[2]

        chapters = book['chapters']
        threads = []
        i = 1
        for chapter in chapters:
            content_file = os.path.join(title, '%s.txt' % chapter['title'].encode('utf-8'))
            if not os.path.exists(content_file):
                thread = DownladThread(i,chapter['url'], content_file)
                thread.start()
                threads.append(thread)
            i += 1

        for thread in threads:
            thread.join()
        if len(threads) != 0:
            mergeChapters(title)

if __name__ == "__main__":
    main()