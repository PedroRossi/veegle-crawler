from crawler import Crawler
from time import sleep
import threading
import os
import re

lock = threading.Lock()

threads = []
reports = []

def crawl_page(link, crawler, file_name, root = 'domains'):
    if not os.path.exists('./' + root + '/' + crawler.name + '/' + file_name):
        sleep(1)
        try:
            r = crawler.request(link).get_soup()
            [s.extract() for s in r('script')]
            crawler.save_to_cache(r.prettify(), file_name, root)
            return True
        except Exception as e:
            print(e)
            pass
    return False

def crawl(domain_name, domain_url, user_agent, search_url_builder, extraction_method, file_name_builder, check_if_valid, use_phantom = False, only_one_page = False, max_visits = 100):
    crawler = Crawler(domain_name, domain_url, user_agent, use_phantom)
    i = 1
    search = search_url_builder(i)
    soup = crawler.request(search)
    links = []
    visited = 0
    valid = 0
    while soup and visited <= max_visits:
        aux = extraction_method(soup)
        for href in aux:
            print(href)
            valid += 1 if check_if_valid(href) else 0
            file_name = file_name_builder(href)
            if crawl_page(href, crawler, file_name, 'domains-hr'):
                visited += 1
                links.append(href)
        if only_one_page:
            break
        i += 1
        search = search_url_builder(i)
        try:
            soup = crawler.request(search)
        except:
            soup = None
    report = "Heuristic: " + domain_name + "\nVisited: " + str(visited) + "\nValid: " + str(valid)
    lock.acquire()
    reports.append(report)
    lock.release()

def crawl_bfs(domain_name, domain_url, user_agent, file_name_builder, check_if_valid, use_phantom = False, max_visits = 100):
    def get_all_anchors(soup):
        ret = []
        for a in soup.find('a'):
            try:
                curr = a['href']
                if curr.find(domain_url) >= 0:
                    curr = curr[len(domain_url):]
                if curr[0] is '/':
                    ret.append(curr)
            except:
                pass
        return ret
    crawler = Crawler(domain_name, domain_url, user_agent, use_phantom)
    visited = 0
    valid = 0
    seen = {}
    links = ['/']
    seen[links[0]] = True
    while len(links) > 0 and visited <= max_visits:
        curr = links[0]
        seen[curr] = True
        print('BFS: \n- Current: ' + curr + '\n- Visited: ' + str(visited) + '\n- Links: ' + str(len(links)) + '\n')
        # print(curr)
        links = links[1:]
        soup = crawler.request(curr)
        if soup is None:
            continue
        for link in get_all_anchors(soup):
            if link not in seen:
                links.append(link)
        # links += [link for link in get_all_anchors(soup) if link not in seen]
        file_name = file_name_builder(curr)
        if crawl_page(curr, crawler, file_name, 'domains-bfs'):
            valid += 1 if check_if_valid(curr) else 0
            visited += 1
    report = "BFS: " + domain_name + "\nVisited: " + str(visited) + "\nValid: " + str(valid)
    lock.acquire()
    reports.append(report)
    lock.release()

def main():
    domains = [
        {
            'domain_name': 'tudogostoso',
            'domain_url': 'http://www.tudogostoso.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/busca?q=&page='+str(i),
            'extraction_method': lambda soup: [link['href'] for link in soup.find('a', 'class', 'box-big-item')],
            'file_name_builder': lambda link: link[link.rfind('/')+1:],
            'check_if_valid': lambda link: re.compile(r'^\/receita\/.*\.html$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'tudoreceitas',
            'domain_url': 'https://www.tudoreceitas.com',
            'user_agent': 'Mediapartners-Google',
            'search_url_builder': lambda i: '/pesquisa/pag/'+str(i),
            'extraction_method': lambda soup: [link[link.rfind('/'):] for link in [link['href'] for link in soup.find('a', 'class', 'titulo--resultado')]],
            'file_name_builder': lambda link: link[1:],
            'check_if_valid': lambda link: re.compile(r'^\/.*receita.*\.html$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'receitasdecomidas',
            'domain_url': 'http://receitasdecomidas.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/page/'+str(i)+'?s',
            'extraction_method': lambda soup: [link[link.rfind('/'):] for link in [link.a['href'] for link in soup.find('article', 'class', 'post')]],
            'file_name_builder': lambda link: link[1:],
            'check_if_valid': lambda link: re.compile(r'^\/.*.html$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'gordelicias',
            'domain_url': 'http://gordelicias.biz',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/index.php/category/receitas-3/page/'+str(i)+'/',
            'extraction_method': lambda soup: [href[href.find('/', 10):] for href in [link.a['href'] for link in soup.find('div', 'class', 'post-media')]],
            'file_name_builder': lambda link: link[link[:len(link)-2].rfind('/')+1:len(link)-1]+'.html',
            'check_if_valid': lambda link: re.compile(r'^\/index\.php\/(\d{4})(\/(\d{2})){2}\/.*\/$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'receitasdemae',
            'domain_url': 'https://www.receitasdemae.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/receitas/page/'+str(i)+'/',
            'extraction_method': lambda soup: [link.a['href'] for link in soup.find('h2', 'class', 'entry-title')],
            'file_name_builder': lambda link: link[10:len(link)-1]+'.html',
            'check_if_valid': lambda link: re.compile(r'^\/receitas\/.*\/$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'receitasig',
            'domain_url': 'http://receitas.ig.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/busca/?q=+#pagina='+str(i),
            'extraction_method': lambda soup: [link[link.find('/', 10):] for link in [link.h5.a['href'] for link in soup.find('div', 'class', 'infos')]],
            'file_name_builder': lambda link: '-'.join([a for a in link.split('/')[1:]]),
            'check_if_valid': lambda link: re.compile(r'^\/.*.html$').match(link) is not None,
            'use_phantom': True,
            'only_one_page': False
        },
        {
            'domain_name': 'receitademinuto',
            'domain_url': 'http://receitasdeminuto.com',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/categoria/receitas/page/'+str(i)+'/',
            'extraction_method': lambda soup: [link[link.find('/', 10):] for link in [link.a['href'] for link in soup.find('h2', 'class', 'postTitle')]],
            'file_name_builder': lambda link: link[1:len(link)-1]+'.html',
            'check_if_valid': lambda link: re.compile(r'^(?!.*(sobre|contato|midia-kit|livro)).*\/$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'comidasebebidasuol',
            'domain_url': 'https://comidasebebidas.uol.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/receitas/?next=0001H4753U'+str((i-1)*36)+'N',
            'extraction_method': lambda soup: [link[link.find('/', 10):] for link in [link.a['href'] for link in soup.find('div', 'class', 'thumbnail-standard-wrapper')]],
            'file_name_builder': lambda link: link[link.rfind('/')+1:] + 'l',
            'check_if_valid': lambda link: re.compile(r'^\/receitas\/(\d{4})(\/(\d{2})){2}\/.*\.htm$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': False
        },
        {
            'domain_name': 'presuntovegetariano',
            'domain_url': 'http://presuntovegetariano.com.br',
            'user_agent': 'veegle',
            'search_url_builder': lambda i: '/receitas-de-a-z/',
            'extraction_method': lambda soup: [link[link.find('/', 10):] for link in [link.strong.a['href'] for link in soup.find('li') if link and link.strong and link.strong.a]],
            'file_name_builder': lambda link: link[link[:len(link)-1].rfind('/'):len(link)-1] + '.html',
            'check_if_valid': lambda link: re.compile(r'^\/receitas\/.*\/$').match(link) is not None,
            'use_phantom': False,
            'only_one_page': True
        }
    ]

    max_to_visit = 100

    for domain in domains:
        t = threading.Thread(
            target=crawl_bfs,
            args=(
                domain['domain_name'],
                domain['domain_url'],
                domain['user_agent'],
                lambda link: link[1:].replace('/', '-')+'.html',
                domain['check_if_valid'],
                domain['use_phantom'],
                max_to_visit
            )
        )
        threads.append(t)
        t.start()

    for domain in domains:
        t = threading.Thread(
            target=crawl,
            args=(
                domain['domain_name'],
                domain['domain_url'],
                domain['user_agent'],
                domain['search_url_builder'],
                domain['extraction_method'],
                domain['file_name_builder'],
                domain['check_if_valid'],
                domain['use_phantom'],
                domain['only_one_page'],
                max_to_visit
            )
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    ret = ''
    for report in reports:
        print(report + '\n')
        ret += report + '\n'

    f = open('./reports-1000.txt', 'w')
    f.write(ret)
    f.close()

if __name__ == "__main__":
    main()