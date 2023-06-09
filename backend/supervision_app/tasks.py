from .celery import app
from job_analyzer.models import JobAdvertisement
from model.pipeline.pipeline import Pipeline
from celery import shared_task
import pandas as pd
from datetime import datetime
import pickle
import sys
sys.path.append("..")
from scrapers import oglaszamy24_scraper, olx_scraper, sprzedajemy_scraper

from pathlib import Path
file_path = Path(__file__).resolve()
DATA_PATH = file_path.parent.parent.parent.joinpath('data')

MODEL_PATH = DATA_PATH.joinpath('model_baseline.pkl')


@shared_task
def scrape_data():

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    pipeline = Pipeline()

    df_olx, df_oglaszamy24, df_sprzedajemy = scrape_data_from_source(
        n=1)

    df = pd.concat([df_olx, df_oglaszamy24, df_sprzedajemy], ignore_index=True)

    X = df[['desc', 'user_registration_date', 'post_creation']]

    x_transformed = pipeline.run(X, DATA_PATH.joinpath('stop_words_polish.txt'))

    df['date_added'] = df['post_creation']
    df['date_of_account_creation'] = df['user_registration_date']

    x_transformed = x_transformed.drop(['desc', 'user_registration_date', 'post_creation'], axis=1)
    df['fake_probability'] = model.predict(x_transformed)

    # write lambda function which will assign priority level based on fake_probability
    # 0.9 - 1 - very high
    # 0.75 - 0.9 - high
    # 0.5 - 0.75 - medium
    # 0.25 - 0.5 - low
    # 0.1 - 0.25 - very low
    df['priority_level'] = df['fake_probability'].apply(lambda x: 'Very High' if x >= 0.9 else 'High' if x >= 0.75 else 'Medium' if x >= 0.5 else 'Low' if x >= 0.25 else 'Very Low')

    df['is_fake'] = df['priority_level'].apply(lambda x: True if x != 'Low' and x != 'Very Low' else False)

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
        date_of_account_creation=row['date_of_account_creation'],
        fake_probability=row['fake_probability'],
        priority_level=row['priority_level'],
        is_fake=row['is_fake'],)
    job.save()

def scrape_data_from_source(n=1):
    df_olx = olx_scraper.OlxScraper.get_df(n)

    df_oglaszamy24 = oglaszamy24_scraper.Oglaszamy24Scraper.get_df(n)

    df_sprzedajemy = sprzedajemy_scraper.create_df(n)

    return df_olx, df_oglaszamy24, df_sprzedajemy
