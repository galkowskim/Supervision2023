from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "supervision_app.settings")
app = Celery('supervision_app',
             broker='redis://',
             backend='rpc://',
             include=['supervision_app.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
