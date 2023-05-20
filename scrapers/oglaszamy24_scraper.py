from bs4 import BeautifulSoup
import requests
from scrapers.scraper import Scraper
import pandas as pd

URL = 'http://www.oglaszamy24.pl/ogloszenia/?std=1&results=1'


def get_urls(n=10, page_limit=25):
    urls = []
    no = 0
    i = 1
    no_page = 1
    new_offers = 'http://www.oglaszamy24.pl/ogloszenia/?std=1&results={no_page}'
    page = requests.get(new_offers)
    soup = BeautifulSoup(page.content, 'html.parser')
    offer = soup.find_all('div', class_='o_single_box')[
        0].find_all('a')[0]['href']
    urls.append(offer)
    while no <= n and no_page <= page_limit:
        try:
            offer = soup.find_all('div', class_='o_single_box')[
                i].find_all('a')[0]['href']
        except:
            no_page += 1
            i = 1
            offer = soup.find_all('div', class_='o_single_box')[
                0].find_all('a')[0]['href']
            new_offers = f'http://www.oglaszamy24.pl/ogloszenia/?std=1&results={no_page}'
            page = requests.get(new_offers)
            soup = BeautifulSoup(page.content, 'html.parser')
            offer = soup.find_all('div', class_='o_single_box')[
                0].find_all('a')[0]['href']
            urls.append(offer)
        offer = soup.find_all('div', class_='o_single_box')[
            i].find_all('a')[0]['href']
        urls.append(offer)
        i += 1
        no += 1
    return urls


class Oglaszamy24Scraper(Scraper):

    def __init__(self, url) -> None:
        self.url = url
        self._run()

    def _run(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        main_div = soup.find_all('div', class_='page_left_col')[0]
        self.title = main_div.find_all('h1', class_='std_h1')[0].text
        self.desc = main_div.find_all('div', id='adv_desc')[0].text
        temp = soup.find_all('div', class_='page_left_col')[
            0].find_all('span', class_='bg_desc')
        temp = [x.text for x in temp if x.text.startswith('Dodano:')]
        self.offer_posted = temp[0][8:] if temp else ''

    @staticmethod
    def get_df(n=10):
        urls = get_urls(n)
        df = pd.DataFrame(
            columns=['title', 'desc', 'offer_posted', 'url'])
        for url in urls:
            try:
                olx = Oglaszamy24Scraper(url)
            except:
                continue
            df = pd.concat([df, pd.DataFrame({'title': [olx.title], 'desc': [olx.desc],
                                              'offer_posted': [olx.offer_posted],
                                              'url': [olx.url]})], ignore_index=True)
        return df

    def print_prop(self) -> str:
        print(f'tytul = {self.title}', end='\n\n')
        print(f'opis = {self.desc}', end='\n\n')
        print(f'oferta od = {self.offer_posted}', end='\n\n')
