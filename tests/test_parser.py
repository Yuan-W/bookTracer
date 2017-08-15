#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from .context import bookTracer
from bookTracer.bookParser import BookParser
from bookTracer.coverParser import CoverParser

class getTitleTestCase(unittest.TestCase):
  def test_zongheng(self):
    url = 'http://book.zongheng.com/showchapter/572378.html'
    title = '天工'.decode('utf-8')
    author = '沙包'.decode('utf-8')
    cover = 'http://static.zongheng.com/upload/cover/2016/06/1464759162830.jpg'
    ori_info = (title, author)
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(ori_info, info)
    cover_parser = CoverParser(url)
    cover_url = cover_parser.getCover()
    self.assertEqual(cover, cover_url)

  def test_biquge(self):
    url = 'http://www.biquge.com.tw/16_16166/'
    title = '永恒剑主'.decode('utf-8')
    author = '滚开'.decode('utf-8')
    cover = 'http://www.biquge.com.tw/files/article/image/16/16166/16166s.jpg'
    ori_info = (title, author)
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(ori_info, info)
    cover_parser = CoverParser(url)
    cover_url = cover_parser.getCover()
    self.assertEqual(cover, cover_url)

  def test_luoqiu(self):
    url = 'http://www.luoqiu.com/read/29515/'
    title = '邪神旌旗'.decode('utf-8')
    author = '楚白'.decode('utf-8')
    cover = 'http://image.luoqiu.com/29/29515/29515s.jpg'
    ori_info = (title, author)
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(ori_info, info)
    cover_parser = CoverParser(url)
    cover_url = cover_parser.getCover()
    self.assertEqual(cover, cover_url)

  def test_ziyouge(self):
    url = 'http://www.ziyouge.com/zy/11/11852/index.html'
    title = '护花小神农'.decode('utf-8')
    author = '八爪章鱼'.decode('utf-8')
    cover = 'http://t.ziyouge.com/11/11852/11852s.jpg'
    ori_info = (title, author)
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(ori_info, info)
    cover_parser = CoverParser(url)
    cover_url = cover_parser.getCover()
    self.assertEqual(cover, cover_url)

def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(getTitleTestCase))
    return testSuite

if __name__ == '__main__':
  mySuit=suite()
  runner=unittest.TextTestRunner(verbosity=2)
  runner.run(mySuit)