from requests_handler import RequestsHandler
from parser_handler import ParserHandler
from selenium import webdriver
from time import sleep
import os

class Crawler():
    
    def __init__(self, name, base_url, agent_name, js_enabled = False):
        self.name = name
        self.requests_handler = RequestsHandler(base_url, agent_name)
        self.parser_handler = ParserHandler()
        self.driver = None
        if js_enabled:
            self.driver = webdriver.PhantomJS('./phantomjs')
            sleep(4)

    def request(self, path):
        try:
            if self.driver:
                self.driver.get(self.requests_handler.base_url + path)
                sleep(2)
                self.parser_handler.parse_page(self.driver.page_source)
            else:
                r = self.requests_handler.get_page(path, 'text/html')
                self.parser_handler.parse_page(r.text)
            return self.parser_handler
        except:
            return None

    def save_to_cache(self, data, file_name, root, is_valid):
        path = './' + root + '/' + self.name + '/' + is_valid + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + file_name, 'w')
        file.write(data)
        file.close()        