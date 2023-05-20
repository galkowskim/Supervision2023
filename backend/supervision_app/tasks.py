from datetime import datetime

from celery import shared_task
from job_analyzer.models import JobAdvertisement
import pickle
# TODO
# from .scrapers import scrape_data_from_source # cos w tym stylu

MODEL_PATH = 'path/to/model'

@shared_task
def scrape_data():

    model = pickle.load(MODEL_PATH)

    data = scrape_data_from_source()  # Your scraping function
    probability = 
    job = JobAdvertisement(
        title=data['title'], content=data['content'], date_added=datetime.now())
    job.save()
