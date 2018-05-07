from crawler import Crawler
import os
import time

def crawl(domain_name, domain_url, user_agent, search_url_builder, extraction_method, file_name_builder):
    
    def crawl_page(link, crawler, file_name):
        if not os.path.exists(crawler.storage_path + file_name):
            time.sleep(1)
            try:
                recipe = crawler.request(link).get_soup()
                [s.extract() for s in recipe('script')]
                crawler.save_to_cache(recipe.prettify(), file_name)
            except:
                pass
            return True
        return False

    crawler = Crawler(domain_name, domain_url, user_agent)
    i = 1
    search = search_url_builder(i)
    soup = crawler.request(search)
    links = []
    while soup and len(links) <= 1000 :
        print(i)
        aux = extraction_method(soup)
        for href in aux:
            file_name = file_name_builder(href)
            if crawl_page(href, crawler, file_name_builder(href)):
                links.append(href)
        i += 1
        search = search_url_builder(i)
        try:
            soup = crawler.request(search)
        except:
            soup = None
    print(len(links))

def main():
    # crawl_tudogostoso()
    # crawl_tudoreceitas()
    # crawl_receitasdecomidas()
    '''
    crawl(
        'tudogostoso',
        'http://www.tudogostoso.com.br',
        'veegle',
        lambda i: '/busca?q=&page='+str(i),
        lambda soup: [link['href'] for link in soup.find('a', 'class', 'box-big-item')],
        lambda link: link[link.rfind('/')+1:]
    )
    crawl(
        'tudoreceitas',
        'https://www.tudoreceitas.com',
        'Mediapartners-Google',
        lambda i: '/pesquisa/pag/'+str(i),
        lambda soup: [link[link.rfind('/'):] for link in [link['href'] for link in soup.find('a', 'class', 'titulo--resultado')]],
        lambda link: link[1:]
    )
    crawl(
        'receitasdecomidas',
        'http://receitasdecomidas.com.br',
        'veegle',
        lambda i: '/page/'+str(i)+'?s',
        lambda soup: [link[link.rfind('/'):] for link in [link.a['href'] for link in soup.find('article', 'class', 'post')]],
        lambda link: link[1:]
    )
    crawl(
        'gordelicias',
        'http://gordelicias.biz',
        'veegle',
        lambda i: '/index.php/category/receitas-3/page/'+str(i)+'/',
        lambda soup: [href[href.find('/', 10):] for href in [link.a['href'] for link in soup.find('div', 'class', 'post-media')]],
        lambda link: link[link[:len(link)-2].rfind('/')+1:len(link)-1]+'.html'
    )
    # ADD PHANTOMJS
    crawl(
        'receitasig',
        'http://receitas.ig.com.br',
        'veegle',
        lambda i: '/busca/?q=+#pagina='+str(i),
        # lambda soup: [link[link.find('/', 10)+1:] for link in [link.h5.a['href'] for link in soup.find('div', 'class', 'infos')]],
        lambda soup: [link for link in soup.find('div', 'class', 'infos')],
        lambda link: link[1:]
    )
    '''
    crawl(
        'receitademinuto',
        'http://receitasdeminuto.com',
        'veegle',
        lambda i: '/categoria/receitas/page/'+str(i)+'/',
        lambda soup: [link[link.find('/', 10):] for link in [link.a['href'] for link in soup.find('h2', 'class', 'postTitle')]],
        lambda link: link[1:len(link)-1]+'.html'
    )

if __name__ == "__main__":
    main()