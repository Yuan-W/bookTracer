#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bookParser import BookParser

class getTitleTestCase(unittest.TestCase):
  def test_zongheng(self):
    url = 'http://book.zongheng.com/book/572378.html'
    title = '天工'.decode('utf-8')
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(title, info)

  def test_biquge(self):
    url = 'http://www.biquge.com.tw/16_16166/'
    title = '永恒剑主'.decode('utf-8')
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(title, info)

  def test_luoqiu(self):
    url = 'http://www.luoqiu.com/read/29515/index.html'
    title = '邪神旌旗'.decode('utf-8')
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(title, info)

  def test_3gxs(self):
    url = 'http://www.3gxs.com/html/54/54549/index.html'
    title = '无限冒险指南'.decode('utf-8')
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(title, info)

  def test_ziyouge(self):
    url = 'http://www.ziyouge.com/zy/11/11852/index.html'
    title = '护花小神农'.decode('utf-8')
    parser = BookParser(url)
    info = parser.getBookInfo()
    self.assertEqual(title, info)

def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(getTitleTestCase))
    return testSuite

if __name__ == '__main__':
  mySuit=suite()
  runner=unittest.TextTestRunner(verbosity=2)
  runner.run(mySuit)