import requests
from urllib.parse import urlparse
from reppy.robots import Robots

class RequestsHandler:
    
    def __init__(self):
        self.domains = {}
    
    def get_page(self, url, expected_content_type = ''):
        url_parsed = urlparse(url)
        
        print(url_parsed)

        if url_parsed.netloc not in self.domains:
            robots_url = url_parsed.scheme+'://'+url_parsed.netloc+'/robots.txt'
            robots = Robots.fetch(robots_url)
            agent = robots.agent('veegle')
            self.domains[url_parsed.netloc] = dict({
                "agent": agent
            })
        agent = self.domains[url_parsed.netloc]['agent']
        print(agent.allowed(url))

        r = requests.get(url)
        if r.ok is not True:
            raise Exception('Error response from server')
        if expected_content_type not in r.headers['Content-Type']:
            raise Exception('Content-Type different from '+expected_content_type)
        return r