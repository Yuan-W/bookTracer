import re
from lxml import etree
from rule import BookRule
from parser_base import Parser

class BookParser(Parser):
    def __init__(self, url):
        Parser.__init__(self, url)
        ruleManager = BookRule('rules.json')
        self._url = url
        self._rule = ruleManager.find(url)
        self.parse(self._rule['charset'])

    def getChapters(self):
        chapters = list()
        protocol = self._url.split('/')[0]
        website = self._url.split('/')[2]
        prefix = protocol + '//' + website

        xpathElements = self._tree.xpath(self._rule['xpath_chapters'])

        for element in xpathElements:
            # print(etree.tostring(element))
            url = element.get('href')
            if url[0] == '/':
                url = prefix + url
            elif url[:len(protocol)] != protocol:
                pageBase = self._url.split('/')[:-1]
                url = ('/').join(pageBase)+'/%s' % url
            
            url = url.split('?')[0]
            url = url.split('#')[0]

            prog = re.compile(self._rule['url_pattern'])

            # print element.text, url
            # print url, prog.match(url)

            if not prog.match(url):
                continue

            title = element.text.replace('/', '\\')
            chapter = {'title':title, 'url':url}
            # print element.text, url
            if chapter not in chapters:
                chapters.append(chapter)

        return chapters

    def getBookInfo(self):
        title_raw = self._tree.xpath("//title/text()")[0]
        match = re.search(self._rule['title_pattern'], title_raw)
        title = match.group(1)
        author_raw = self._tree.xpath(self._rule['xpath_author'])[0]
        match = re.search(self._rule['author_pattern'], author_raw)
        author = match.group(1)
        # print title
        return title, author

    