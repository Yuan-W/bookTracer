#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import threading
import os, glob
from contentParser import ContentParser
import codecs
from yattag import Doc, indent
from shutil import copyfile
import urllib2

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
    f.write(content.strip('\n'))
    f.close()
    print "Exiting thread %d" % self._threadID

def generatTxtBook(book):
  title = book['title'].encode('utf-8')
  with open('%s.txt' % title, 'w') as outfile:
    outfile.write('%s\r\n' % title)
    outfile.write('\r\n%s' % book['author'].encode('utf-8'))

    for chapter in book['chapters']:
      content_file = os.path.join(title, '%s.txt' % chapter['title'].encode('utf-8'))
      with open(content_file) as infile:
        outfile.write('\r\n\r\n')
        outfile.write(chapter['title'].encode('utf-8'))
        outfile.write('\r\n\r\n')
        outfile.write(infile.read())

#########################################
#  Files for Kindlegen
#########################################

def generateTOC(path, book):
  doc, tag, text = Doc().tagtext()
  doc.asis('<!DOCTYPE html>')
  with tag('html', lang='zh'):
    with tag('head'):
      doc.stag('meta', ('http-equiv', 'Content-Type'), content='text/html; charset=utf-8')
      with tag('title'):
        text('Table of Contents')
      doc.stag('link', rel='stylesheet', href='style.css', type='text/css')
    with tag('body'):
      with tag('div', id='toc'):
        with tag('h1'):
          text('Table of Contents')
        with tag('ul'):
          for i, chapter in enumerate(book['chapters']):
            with tag('li'):
              with tag('a', href='text.html#ch%d' % (i+1)):
                text(chapter['title'])

  result = indent(doc.getvalue(), newline = '\r\n')

  file_name = os.path.join(path, 'toc.html')
  with open(file_name, 'w') as outfile:
    outfile.write(result.encode('UTF-8'))

def generateContent(path, book):
  doc, tag, text = Doc().tagtext()
  doc.asis('''<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">''')
  with tag('html', lang='zh'):
    with tag('head'):
      doc.stag('meta', ('http-equiv', 'Content-Type'), content='text/html; charset=utf-8')
      with tag('title'):
        text(book['title'].encode('utf-8'))
      doc.stag('link', rel='stylesheet', href='style.css', type='text/css')
    with tag('body'):
      with tag('div', id='content'):
        for i, chapter in enumerate(book['chapters']):
          with tag('div', id='#ch%d' % (i+1)):
            with tag('h2'):
              text(chapter['title'].encode('utf-8'))
            content_file = os.path.join(book['title'].encode('utf-8'), '%s.txt' % chapter['title'].encode('utf-8'))
            with open(content_file) as infile:
              file_content = infile.readlines()
              for line in file_content:
                with tag('p'):
                  text(line)
  
  file_name = os.path.join(path, 'text.html')
  with open(file_name, 'w') as outfile:
    outfile.write(doc.getvalue())

def generateNCX(path, book):
  doc, tag, text = Doc().tagtext()
  doc.asis('<?xml version="1.0"?>')
  doc.asis('''<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
   "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">''')
  doc.asis('<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">')
  doc.stag('head')
  with tag('docTitle'):
    with tag('text'):
      text(book['title'])
  with tag('navMap'):
      with tag('navPoint', id='navpoint-1',playOrder='1'):
        with tag('navLabel'):
          with tag('text'):
            text('Table of Contents')
        doc.stag('content', src='toc.html#toc')
      for i, chapter in enumerate(book['chapters']):
        index = i + 2
        with tag('navPoint', id='navpoint-%d' % index, playOrder='%d' % index):
          with tag('navLabel'):
            with tag('text'):
              text(chapter['title'])
          doc.stag('content', src='text.html#ch%d' % (i+1))

  result = indent(doc.getvalue(), newline = '\r\n')

  file_name = os.path.join(path, 'toc.ncx')
  with open(file_name, 'w') as outfile:
    outfile.write(result.encode('UTF-8'))

def generateOPF(path, book):
  doc, tag, text = Doc().tagtext()
  doc.asis('<?xml version="1.0" encoding="utf-8"?>')
  with tag('package', ('unique-identifier', 'uid'), ('xmlns:opf', 'http://www.idpf.org/2007/opf'),
   ('xmlns:asd', 'http://www.idpf.org/asdfaf')):
    with tag('metadata'):
      with tag('dc-metadata', ('xmlns:dc', 'http://purl.org/metadata/dublin_core'), 
        ('xmlns:oebpackage', 'http://openebook.org/namespaces/oeb-package/1.0/')):
        with tag('dc:Title'):
          text(book['title'])
        with tag('dc:Language'):
          text('zh')
        with tag('dc:Creator'):
          text(book['author'])
        # with tag('dc:Copyrights'):
        #   text('NA')
        with tag('dc:Publisher'):
          text('Yuan')
        with tag('x-metadata'):
          with tag('EmbeddedCover'):
            text('cover.jpg')
    with tag('manifest'):
      doc.stag('item', ('media-type', 'text/x-oeb1-document'), id='content', href='toc.html')
      doc.stag('item', ('media-type', 'application/x-dtbncx+xml'), id='ncx', href='toc.ncx')
      doc.stag('item', ('media-type', 'text/x-oeb1-document'), id='text', href='text.html')
    with tag('spine', toc='ncx'):
      doc.stag('itemref', idref='content')
      doc.stag('itemref', idref='text')
    with tag('guide', toc='ncx'):
      doc.stag('reference', type='toc', title='Table of Contents', href='toc.html')
      doc.stag('reference', type='text', title='Book', href='text.html')
  

  result = indent(doc.getvalue(), newline = '\r\n')

  file_name = os.path.join(path, '%s.opf' % book['title'].encode('utf-8'))
  with open(file_name, 'w') as outfile:
    outfile.write(result.encode('UTF-8'))


def generatKindleBook(book):
  title = book['title'].encode('utf-8')
  path = 'Kindle/%s' % title
  if not os.path.isdir(path):
    os.makedirs(path)
    copyfile('style.css', '%s/style.css' % path)
    copyfile('%s/cover.jpg' % title, '%s/cover.jpg' % path)

  generateTOC(path, book)
  generateContent(path, book)
  generateNCX(path, book)
  generateOPF(path, book)

def mergeChapters(title, output_format):
  book_file = os.path.join('book', '%s.json' % title)

  with open(book_file, 'r') as fp:
    book = json.load(fp)

  if output_format == 'txt':
    generatTxtBook(book)
  elif output_format == 'kindle':
    generatKindleBook(book)
  

def main():
  path = 'book'
  output_format = 'kindle'

  # file = os.path.join('book', '%s.json' % title)

  for file in glob.glob("%s/*.json" % path):
    title_ext = os.path.basename(file)
    title = os.path.splitext(title_ext)[0]
    if not os.path.isdir(title):
      os.mkdir(title)

    with open(file, 'r') as fp:
      book = json.load(fp)

    cover = '%s/cover.jpg' % title
    if not os.path.exists(cover):
       img = urllib2.urlopen(book['cover'])
       with open(cover, 'wb') as fp:
        fp.write(img.read())

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
    # if len(threads) != 0:
    mergeChapters(title, output_format)

if __name__ == "__main__":
  main()