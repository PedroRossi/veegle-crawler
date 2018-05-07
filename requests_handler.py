import requests
from reppy.robots import Robots

# TODO
class RequestsHandler:
    
    def __init__(self, base_url, agent_name):
        self.base_url = base_url
        self.robots = Robots.fetch(base_url+'/robots.txt')
        self.agent = self.robots.agent(agent_name)
        self.session = requests.session()

    def get_page(self, path, expected_content_type = ''):
        url = self.base_url + path
        if self.agent.allowed(url) is not True:
            raise Exception('Crawling not allowed for this agent')
        r = self.session.get(url)
        if r.ok is not True:
            raise Exception('Error response from server')
        if expected_content_type not in r.headers['Content-Type']:
            raise Exception('Content-Type different from ' + expected_content_type)
        return r