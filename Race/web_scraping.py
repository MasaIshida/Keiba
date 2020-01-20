import requests
from bs4 import BeautifulSoup
import lxml

from Scraping.access_website import Scraping


class RaceScraping(Scraping):

    def __init__(self, url):
        super(RaceScraping, self).__init__(url)

    def create_header_data(self, year, month, jyo):
        setter_list = self.value_action(year, month, jyo)
        self.header_data = {
            'pid': 'race_list',
            'start_year': setter_list[0],
            'start_mon': setter_list[1],
            'end_year': setter_list[0],
            'end_mon': setter_list[1],
            'jyo[]': setter_list[2],
            'kyori_min': '',
            'kyori_max': '',
            'sort': 'data',
            'list': '100'
        }

    def request_post_method(self):
        print(self.header_data)
        re = requests.post(self.url, data=self.header_data)
        bs = BeautifulSoup(re.content, "lxml")
        return bs

    def value_action(self, year, month, jyo):
        edit_list = [year, month, jyo]
        setter_list = []
        for data in edit_list:
            if data < 10:
                data = "0" + str(data)
            else:
                data = str(data)
            setter_list.append(data)
        return setter_list


class RaceDetailsScraping(Scraping):

    def __init__(self, url):
        super(RaceDetailsScraping, self).__init__(url)
