from requests_handler import RequestsHandler
from parser_handler import ParserHandler
import os

# TODO
'''
- 1000 pages per domain
'''
class Crawler():
    
    def __init__(self, name, base_url, agent_name):
        self.name = name
        self.storage_path = './domains/' + name + '/'
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        self.requests_handler = RequestsHandler(base_url, agent_name)
        self.parser_handler = ParserHandler()

    def request(self, path):
        try:
            r = self.requests_handler.get_page(path, 'text/html')
            self.parser_handler.parse_page(r.text)
            return self.parser_handler
        except:
            return None

    def save_to_cache(self, data, file_name):
        file = open(self.storage_path + file_name, 'w')
        file.write(data)
        file.close()

        