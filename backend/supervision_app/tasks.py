from .celery import app
from job_analyzer.models import JobAdvertisement
from celery import shared_task
import pandas as pd
from datetime import datetime
import pickle
import sys
sys.path.append("..")
from scrapers import oglaszamy24_scraper, olx_scraper, sprzedajemy_scraper


MODEL_PATH = '/home/galkowskim/Desktop/Supervision2023/model.sav'


@shared_task
def scrape_data():

    # model = pickle.load(MODEL_PATH)

    df_olx, df_oglaszamy24, df_sprzedajemy = scrape_data_from_source(
        n=2)  # Your scraping function

    df = pd.concat([df_olx, df_oglaszamy24, df_sprzedajemy], ignore_index=True)

    # df['fake_probability'] = model.predict(...)
    df['fake_probability'] = 0.5

    df['date_added'] = datetime.now()


    for index, row in df.iterrows():
        add_job_to_db(row)

def add_job_to_db(row):

    if JobAdvertisement.objects.filter(source_page=row['url']).exists():
        return

    job = JobAdvertisement.objects.create(
        title=row['title'],
        content=row['desc'],
        date_added=row['date_added'],
        source_page=row['url'],
        date_of_account_creation=datetime.now(),
        fake_probability=row['fake_probability'])

    job.save()

def scrape_data_from_source(n=1):
    df_olx = olx_scraper.OlxScraper.get_df(n)

    df_oglaszamy24 = oglaszamy24_scraper.Oglaszamy24Scraper.get_df(n)

    df_sprzedajemy = sprzedajemy_scraper.create_df(n)

    return df_olx, df_oglaszamy24, df_sprzedajemy
