from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime

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
            except:
                continue
        offers_scraped += 60
    return list(page_urls)

URL = 'https://sprzedajemy.pl/wszystkie-ogloszenia?items_per_page=60'

def user_registration_date_to_datetime(date_string):
    month_str = date_string.split(' ')[0]
    year = int(date_string.split(' ')[1])
    day = 1
    month_str_dict = {
        'Sty' : 1,
        'Lut' : 2,
        'Mar' : 3,
        'Kwi' : 4,
        'Maj' : 5,
        'Cze' : 6,
        'Lip' : 7,
        'Sie' : 8,
        'Wrz' : 9,
        'Paź' : 10,
        'Lis' : 11,
        'Gru' : 12
    }
    date = pd.to_datetime(f'{year}-{month_str_dict[month_str]}-{day}')
    return date

def post_creation_to_date(date_string):
    month_str = date_string.split(' ')[1]
    year = datetime.datetime.today().year
    day = int(date_string.split(' ')[0])
    # hour = int(date_string.split(' ')[0])
    month_str_dict = {
        'Sty' : 1,
        'Lut' : 2,
        'Mar' : 3,
        'Kwi' : 4,
        'Maj' : 5,
        'Cze' : 6,
        'Lip' : 7,
        'Sie' : 8,
        'Wrz' : 9,
        'Paź' : 10,
        'Lis' : 11,
        'Gru' : 12
    }
    date = pd.to_datetime(f'{year}-{month_str_dict[month_str]}-{day}')
    if date > pd.to_datetime('today'):
        date = date - pd.DateOffset(years=1)
    return date

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
            except:
                continue
        offers_scraped += 60
    return list(page_urls)

def create_df(n = 1000):
    page_urls = create_url_list(n)
    df = pd.DataFrame(columns=['title', 'desc', 'user_registration_date', 'post_creation', 'user_offers', 'lat', 'lon', 'city', 'url'])

    for offer_url in page_urls:
        try:
            page = requests.get(offer_url)
            soup = BeautifulSoup(page.content, "html.parser")
            description = soup.find('div', class_='offerDescription').get_text().replace('\n', ' ').replace('\t', ' ').replace('\r', ' ').replace('  ', ' ')
            title = soup.find('span', class_='isUrgentTitle').get_text()
            active_since = soup.find('span', class_='active-since').get_text().split('od ')[1]

            user_offers = soup.find('a', class_='user-offers-link').find('span').get_text()
            no_user_offers = int(user_offers.split('(')[1].split(')')[0])


            additional_info = soup.find('ul', class_='offerAdditionalInfo')

            geo = soup.find('ul', class_='offerAdditionalInfo').find('span')
            city = geo.find('a', class_='locationName').get_text()
            geo_str = soup.find('ul', class_='offerAdditionalInfo').find('span').attrs['data-coordinates']
            lat = float(geo_str.split(',')[0].split(':')[1])
            lon = float(geo_str.split(',')[1].split(':')[1])

            
            upload_date = additional_info.find_all('li')[1].get_text()
        except:
            continue

        row = pd.DataFrame({'title': title, 'desc': description, 'user_registration_date': active_since,
                            'post_creation': upload_date, 'user_offers': no_user_offers,
                            'lat':lat, 'lon':lon, 'city':city, 'url': offer_url,}, index=[0])

        df = pd.concat([df, row])
    
    df['user_registration_date'] = df['user_registration_date'].apply(user_registration_date_to_datetime)
    df['post_creation'] = df['post_creation'].apply(post_creation_to_date)

    return df.reset_index(drop=True)

