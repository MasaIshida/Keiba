import requests
from bs4 import BeautifulSoup
import time
import lxml


class Scraping(object):

    def __init__(self, url):
        self.url = url

    def request_get_method(self):
        try:
            re = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            time.sleep(600)
            re = requests.get(self.url)
        bs = BeautifulSoup(re.content, "lxml")
        return bs

    def request_post_method(self):
        try:
            re = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            # 最大数を超えたときの為に
            time.sleep(600)
            re = requests.get(self.url)
        bs = BeautifulSoup(re.content, "lxml")
        return bs
