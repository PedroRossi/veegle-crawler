from requests_handler import RequestsHandler
from parser_handler import ParserHandler

def main():
    rh = RequestsHandler()
    rh.get_page('http://www.tudogostoso.com.br/robots.txt', 'text/plain')
    rh.get_page('http://www.tudogostoso.com.br/usuario/1-tudo-gostoso/', 'text/html')
    rh.get_page('http://www.tudogostoso.com.br/receita/256-camarao-com-requeijao.html', 'text/html')
    data = rh.get_page('http://www.tudogostoso.com.br/busca?q=camar%C3%A3o', 'text/html')
    ParserHandler.parse_page(data.text)

if (__name__ == "__main__"):
    main()