import urllib2
import re
import chardet
from lxml import etree
from HTMLParser import HTMLParser

class MyHTMLParser: 
    def loadPage(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')]
        resource = opener.open(url)

        return resource.read()

    def detectCharset(self, url):
        content = self.loadPage(url)
        return chardet.detect(content)['encoding']

    def getHTMLElementTree(self, url, charset):
        htmlContent = self.loadPage(url)

        parser = etree.HTMLParser(encoding=charset)
        tree = etree.fromstring(htmlContent, parser)
        return tree

    def parseChapters(self, book, rule):
        chapters = list()
        protocol = book['url'].split('/')[0]
        website = book['url'].split('/')[2]
        prefix = protocol + '//' + website

        htmlTree = self.getHTMLElementTree(book['url'], rule['charset'])

        xpathElements = htmlTree.xpath(rule['xpathString'])

        for element in xpathElements:
            # print(etree.tostring(element))
            url = element.get('href')
            if url[0] == '/':
                url = prefix + url
            elif url[:len(protocol)] != protocol:
                pageBase = book['url'].split('/')[:-1]
                url = ('/').join(pageBase)+'/%s' % url
            
            url = url.split('?')[0]
            url = url.split('#')[0]

            prog = re.compile(rule['pattern'])

            # print url, prog.match(url)

            if not prog.match(url):
                continue

            title = element.text
            chapter = {'title':title, 'url':url}
            if chapter not in chapters:
                chapters.append(chapter)

        return chapters

    def parseContent(self, url, rule):
        htmlTree = self.getHTMLElementTree(url, rule['charset'])

        # print(etree.tostring(htmlTree))

        xpathElements = htmlTree.xpath(rule['xpathContent'])

        # for element in xpathElements:
        #     print element 

        # texts = [element.text for element in xpathElements]
        content = '\n\r'.join(xpathElements)
        # content.replace('r'.encode(rule['charset']), '')
        # print content.decode(rule['charset'])
        # content = content.replace('\\r', '')

        return content

    