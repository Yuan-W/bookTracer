import re
from lxml import etree
from rule import BookRule
from parser_base import Parser

class ContentParser(Parser):
    def __init__(self, url):
        Parser.__init__(self, url)
        ruleManager = BookRule('rules.json')
        self._rule = ruleManager.find(url)
        self.parse(self._rule['charset'])

    def getContent(self):
        xpathElements = self._tree.xpath(self._rule['xpath_content'])

        # for element in xpathElements:
        #     print element 

        contents = [c for c in xpathElements if c != '\r\n']

        # for c in contents:
        #     print '*'*40
        #     # if '\n' in element:
        #     #     yield element
        #     #     continue
        #     print repr(c)
        content = '\r\n'.join(contents)
        content = content.replace('\r\n\r\n', '\r\n')
        # content.replace('r'.encode(rule['charset']), '')
        # print content.decode(rule['charset'])
        # content = content.replace('\\r', '')

        return content