from urllib import urlopen
from lxml import etree

class HTMLParser: 
    def getHTMLElementTree(self, url):
        htmlContent = urlopen(url).read()
        parser = etree.HTMLParser()
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
            url = element.get('href')
            if url[0] == '/':
                url = prefix + url
            elif not url.startswith(prefix):
                continue
            title = element.text
            url = url.split('?')[0]
            url = url.split('#')[0]
            splitedLink = url.split('/')

            if splitedLink[rule['urlFilterIndex']] != rule['urlFilterText']:
                continue
            chapter = {'title':title, 'url':url}
            if chapter not in chapters:
                chapters.append(chapter)

        return chapters