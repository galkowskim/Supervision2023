from datetime import datetime

from celery import shared_task
from job_analyzer.models import JobAdvertisement
import pickle
from ...scrapers import olx_scraper, sprzedajemy_scraper, oglaszamy24_scraper
import pandas as pd

# TODO
# from .scrapers import scrape_data_from_source # cos w tym stylu

MODEL_PATH = 'model.sav'

@shared_task
def scrape_data():

    model = pickle.load(MODEL_PATH)

    df_olx, df_oglaszamy24, df_sprzedajemy = scrape_data_from_source(n=2)  # Your scraping function

    df = pd.concat([df_olx, df_oglaszamy24, df_sprzedajemy], ignore_index=True)

    #df['fake_probability'] = model.predict(...)
    df['fake_probability'] = 0.5

    df['date_added'] = datetime.now()

    job = JobAdvertisement.objects.create(
        title=df['title'],
        content=df['desc'],
        date_added=df['date_added'],
        source_page=df['url'],
        date_of_account_creation=datetime.now(),
        fake_probability=df['fake_probability'])

    job.save()



def scrape_data_from_source(n=10):
    df_olx = olx_scraper.OlxScraper.get_df(n)

    df_oglaszamy24 = oglaszamy24_scraper.Oglaszamy24Scraper.get_df(n)

    df_sprzedajemy = sprzedajemy_scraper.create_df(n)

    return df_olx, df_oglaszamy24, df_sprzedajemy