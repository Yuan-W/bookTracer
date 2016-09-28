import urllib2
import re
from lxml import etree

class MyHTMLParser: 
    def getHTMLElementTree(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')]
        opener.encoding = "utf-8"
        htmlContent = opener.open(url).read()

        parser = etree.HTMLParser(encoding="utf-8")
        tree = etree.fromstring(htmlContent, parser)
        return tree

    def parseChapters(self, book, rule, chapterCount=0):
        chapters = list()
        protocol = book['url'].split('/')[0]
        website = book['url'].split('/')[2]
        prefix = protocol + '//' + website

        htmlTree = self.getHTMLElementTree(book['url'])

        xpathElements = htmlTree.xpath(rule['xpathString'])

        for element in xpathElements:
            # print(etree.tostring(element))
            url = element.get('href')
            if url[0] == '/':
                url = prefix + url
            elif not url.startswith(prefix):
                continue
            title = element.text
            url = url.split('?')[0]
            url = url.split('#')[0]
            splitedLink = url.split('/')

            prog = re.compile(rule['pattern'])

            if not prog.match(url):
                continue
            chapter = {'title':title, 'url':url}
            if chapter not in chapters:
                chapters.append(chapter)

    def parseContent(self, url, rule):
        htmlTree = self.getHTMLElementTree(url)

        xpathElements = htmlTree.xpath(rule['xpathContent'])

        texts = [element.text for element in xpathElements]
        content = '\n\r'.join(texts)

        return content