import requests
from bs4 import BeautifulSoup
import lxml

from Scraping.access_website import Scraping


class NowRaceScraping(Scraping):

    def __init__(self, url):
        super(NowRaceScraping, self).__init__(url)
