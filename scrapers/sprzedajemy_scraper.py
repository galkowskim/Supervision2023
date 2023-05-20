from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://sprzedajemy.pl/wszystkie-ogloszenia?items_per_page=60'

def create_url_list(n = 1000):
    offers_to_scrape = n
    offers_scraped = 0

    page_urls = set()
    while offers_scraped <= offers_to_scrape:
        page_url = URL + '&offset=' + str(offers_scraped)
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        page_offers = soup.find_all('ul', class_='list normal')[0].find_all('article', class_='element')
        for offer in page_offers:
            try:
                offer_url = offer.find('a')['href']
                page_urls.add('https://sprzedajemy.pl'+offer_url)
                offers_scraped += 1
            except:
                continue
    return list(page_urls)

def create_df(n = 1000):
    page_urls = create_url_list(n)
    df = pd.DataFrame(columns=['title', 'desc', 'user_registered', 'offer_posted', 'url'])

    for offer_url in page_urls:
        page = requests.get(offer_url)
        soup = BeautifulSoup(page.content, "html.parser")
        description = soup.find('div', class_='offerDescription').get_text().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('  ', ' ')
        title = soup.find('span', class_='isUrgentTitle').get_text()
        active_since = soup.find('span', class_='active-since').get_text().split('od ')[1]

        user_offers = soup.find('a', class_='user-offers-link').find('span').get_text()
        no_user_offers = int(user_offers.split('(')[1].split(')')[0])

        additional_info = soup.find('ul', class_='offerAdditionalInfo')
        upload_date = additional_info.find_all('li')[1].get_text()

        row = pd.DataFrame({'title': title, 'desc': description, 'user_registered': active_since, 'offer_posted': upload_date, 'url': offer_url}, index=[0])

        df = pd.concat([df, row])

    return df
