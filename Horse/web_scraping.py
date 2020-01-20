import requests
from bs4 import BeautifulSoup
import lxml

from Scraping.access_website import Scraping


class HorseScraping(Scraping):

    def __init__(self, url):
        super(HorseScraping, self).__init__(url)

    def create_target_url(self):
        try:
            if "ped/" in self.url:
                self.url = "https://db.netkeiba.com" + self.url.replace("ped/", "")
        except TypeError as e:
            self.url = None
            return self.url
        return self.url
