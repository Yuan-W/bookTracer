import urllib2
from lxml import etree

class Parser:
    def __init__(self, url, charset=None):
        self._content = self.loadPage(url)

    def parse(self, charset):
        parser = etree.HTMLParser(encoding=charset)
        self._tree = etree.fromstring(self._content, parser)
        
    def loadPage(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')]
        resource = opener.open(url, timeout=10)
        return resource.read()

    def getCharset(self):
        return chardet.detect(self._content)['encoding']