import re
from lxml import etree
from rule import BookRule
from parser_base import Parser

class CoverParser(Parser):
  def __init__(self, url):
    ruleManager = BookRule('rules.json')
    self._rule = ruleManager.find(url)
    if 'index_pattern' in self._rule:
      match = re.search(self._rule['index_pattern'], url)
      index = match.group(1)
      book_page = self._rule['book_page_pattern'].replace('(index)', index)
      self._url = book_page
    else:
      self._url = url

    Parser.__init__(self, self._url)
    self.parse(self._rule['charset'])

  def getCover(self):
    cover = self._tree.xpath(self._rule['xpath_cover'])[0]
    if not cover.startswith('http'):
      if self._url.endswith('/'):
        base = self._url.split('/')[:-2]
      else:
        base = self._url.strip().split('/')[:-1]
      cover = ('/').join(base)+'%s' % cover
      
    return cover
    