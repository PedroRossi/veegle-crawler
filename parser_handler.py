from bs4 import BeautifulSoup

class ParserHandler:
    
    def __init__(self):
        self.soup = None

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.soup = soup

    def get_soup(self):
        return self.soup

    def find(self, tag, attr = '', txt = ''):
        res = []
        for element in self.soup.find_all(tag):
            try:
                if attr is not '':
                    if element[attr] and element[attr].count(txt) is not 0:
                        res.append(element)
                else:
                    res.append(element)
            except KeyError:
                pass
        return res

    def find_one(self, tag, attr, txt):
        for element in self.soup.find_all(tag):
            try:
                if element[attr] and element[attr].count(txt) is not 0:
                    return element
            except KeyError:
                pass
        return None