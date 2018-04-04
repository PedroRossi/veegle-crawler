from bs4 import BeautifulSoup

class ParserHandler:
    
    @staticmethod
    def parse_page(page):
        soup = BeautifulSoup(page, 'html.parser')
        for div in soup.find_all('div'):
            try:
                if div['class'] and div['class'].count('ingredients-info') is not 0:
                    print('achou')
            except KeyError:
                pass