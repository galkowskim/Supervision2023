from bs4 import BeautifulSoup
import requests
import pandas as pd
from scrapers.scraper import Scraper

URL = 'https://olx.pl'


def get_urls(n=10, page_limit=25):
    '''
    n - number of offers to scrape
    page_limit - number of pages to scrape
    '''
    urls = []
    no = 0
    i = 1
    no_page = 1
    new_offers = f'https://www.olx.pl/oferty/?page={no_page}&search%5Border%5D=created_at%3Adesc'
    page = requests.get(new_offers)
    soup = BeautifulSoup(page.content, 'html.parser')
    offer = soup.find_all('a', class_='css-rc5s2u')[0]['href']
    urls.append(offer)
    while no <= n and no_page <= page_limit:
        try:
            offer = soup.find_all('a', class_='css-rc5s2u')[i]['href']
        except:
            no_page += 1
            i = 1
            new_offers = f'https://www.olx.pl/oferty/?page={no_page}&search%5Border%5D=created_at%3Adesc'
            page = requests.get(new_offers)
            soup = BeautifulSoup(page.content, 'html.parser')
            offer = soup.find_all('a', class_='css-rc5s2u')[0]['href']
            urls.append(offer)
        offer = soup.find_all('a', class_='css-rc5s2u')[i]['href']
        urls.append(offer)
        i += 1
        no += 1
    return urls


month_to_digit1 = {
    'stycznia': '01',
    'lutego': '02',
    'marca': '03',
    'kwietnia': '04',
    'maja': '05',
    'czerwca': '06',
    'lipca': '07',
    'sierpnia': '08',
    'września': '09',
    'października': '10',
    'listopada': '11',
    'grudnia': '12'
}

month_to_digit2 = {
    'styczeń': '01',
    'luty': '02',
    'marzec': '03',
    'kwiecień': '04',
    'maj': '05',
    'czerwiec': '06',
    'lipiec': '07',
    'sierpień': '08',
    'wrzesień': '09',
    'październik': '10',
    'listopad': '11',
    'grudzień': '12'
}


class OlxScraper(Scraper):
    def __init__(self, url) -> None:
        self.TODAY = '20 maja 2023'
        self.url = url
        self._run()

    def _run(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp = soup.find_all('span', class_='css-19yf5ek')[0].text
        self.offer_posted = temp if 'Dzisiaj' not in temp else self.TODAY
        self.offer_posted = self.offer_posted.split(
            ' ')[2] + '-' + month_to_digit1[self.offer_posted.split(' ')[1]] + '-' + self.offer_posted.split(' ')[0]

        main_div = soup.find_all('div', class_='css-1wws9er')[0]
        self.desc = main_div.find_all('div', class_='er34gjf0')[0].text
        self.title = main_div.find_all('h1', class_='css-1soizd2')[0].text
        self.user_register = soup.find_all(
            'div', class_='css-16h6te1')[0].text[13:]
        self.user_register = self.user_register.split(
            ' ')[1] + '-' + month_to_digit2[self.user_register.split(' ')[0]] + '-' + '01'

    def get_df(n=10):
        urls = [URL + x for x in get_urls(n) if 'http' not in x]
        df = pd.DataFrame(
            columns=['title', 'desc', 'user_registration_date', 'post_creation', 'url'])
        for url in urls:
            try:
                olx = OlxScraper(url)
            except:
                continue
            df = pd.concat([df, pd.DataFrame({'title': [olx.title], 'desc': [olx.desc],
                                              'user_registration_date': [olx.user_register],
                                              'post_creation': [olx.offer_posted],
                                              'url': [olx.url]})], ignore_index=True)
        return df

    def print_prop(self) -> str:
        print(f'tytul = {self.title}', end='\n\n')
        print(f'opis = {self.desc}', end='\n\n')
        print(f'od kiedy uzytkownik = {self.user_register}', end='\n\n')
        print(f'oferta od = {self.offer_posted}', end='\n\n')
