#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from rule import BookRule

ruleFile= 'rules.json'

class GetRuleTestCase(unittest.TestCase):
  def setUp(self):
    self.rules = BookRule(ruleFile)

  def testGetRule(self):
    website = 'book.zongheng.com'
    url_pattern = "http:\\/\\/book.zongheng.com\\/chapter\\/\\d+\\/\\d+.html"
    charset = "utf-8"
    xpathContent = "//div[@id=\"chapterContent\"]//p/text()"
    xpathChapters  = "//div[@class=\"read_con\"]//a[@href]"
    title_pattern = "(.*)无弹窗.*".decode('utf-8')
    rule = self.rules.find(website)

    self.assertEqual(rule['website'], website)
    self.assertEqual(rule['url_pattern'], url_pattern)
    self.assertEqual(rule['charset'], charset)
    self.assertEqual(rule['xpath_content'], xpathContent)
    self.assertEqual(rule['xpath_chapters'], xpathChapters)
    self.assertEqual(rule['title_pattern'], title_pattern)

  def testGetRuleWithHTTP(self):
    website = 'book.zongheng.com'
    url_pattern = "http:\\/\\/book.zongheng.com\\/chapter\\/\\d+\\/\\d+.html"
    charset = "utf-8"
    xpathContent = "//div[@id=\"chapterContent\"]//p/text()"
    xpathChapters  = "//div[@class=\"read_con\"]//a[@href]"
    title_pattern = "(.*)无弹窗.*".decode('utf-8')

    url = 'http://book.zongheng.com/'
    rule = self.rules.find(url)

    self.assertEqual(rule['website'], website)
    self.assertEqual(rule['url_pattern'], url_pattern)
    self.assertEqual(rule['charset'], charset)
    self.assertEqual(rule['xpath_content'], xpathContent)
    self.assertEqual(rule['xpath_chapters'], xpathChapters)
    self.assertEqual(rule['title_pattern'], title_pattern)

  def testGetRuleForBookPage(self):
    website = 'book.zongheng.com'
    url_pattern = "http:\\/\\/book.zongheng.com\\/chapter\\/\\d+\\/\\d+.html"
    charset = "utf-8"
    xpathContent = "//div[@id=\"chapterContent\"]//p/text()"
    xpathChapters  = "//div[@class=\"read_con\"]//a[@href]"
    title_pattern = "(.*)无弹窗.*".decode('utf-8')

    url = 'http://book.zongheng.com/book/572378.html'
    rule = self.rules.find(url)

    self.assertEqual(rule['website'], website)
    self.assertEqual(rule['url_pattern'], url_pattern)
    self.assertEqual(rule['charset'], charset)
    self.assertEqual(rule['xpath_content'], xpathContent)
    self.assertEqual(rule['xpath_chapters'], xpathChapters)
    self.assertEqual(rule['title_pattern'], title_pattern)

class UrlMatchingTestCase(unittest.TestCase):
  def setUp(self):
    self.rules = BookRule(ruleFile)

  def test_zongheng(self):
    url = 'http://book.zongheng.com/chapter/572378/32963122.html'
    rule = self.rules.find(url)
    self.assertRegexpMatches(url, rule['url_pattern'])

  def test_biquge(self):
    url = 'http://www.biquge.com.tw/16_16166/5834271.html'
    rule = self.rules.find(url)
    self.assertRegexpMatches(url, rule['url_pattern'])

  def test_luoqiu(self):
    url = 'http://www.luoqiu.com/read/29515/8118902.html'
    rule = self.rules.find(url)
    self.assertRegexpMatches(url, rule['url_pattern'])

  # def test_3gxs(self):
  #   url = 'http://www.3gxs.com/html/54/54549/10818563.html'
  #   rule = self.rules.find(url)
  #   self.assertRegexpMatches(url, rule['url_pattern'])

  def test_ziyouge(self):
    url = 'http://www.ziyouge.com/zy/11/11852/3321892.html'
    rule = self.rules.find(url)
    self.assertRegexpMatches(url, rule['url_pattern'])

def suite():
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(GetRuleTestCase))
    testSuite.addTest(unittest.makeSuite(UrlMatchingTestCase))
    return testSuite

if __name__ == '__main__':
  mySuit=suite()
  runner=unittest.TextTestRunner(verbosity=2)
  runner.run(mySuit)