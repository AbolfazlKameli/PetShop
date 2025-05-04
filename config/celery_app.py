import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.core.base')

app = Celery('PetShop')

app.autodiscover_tasks()

app.config_from_object('config.settings.celery_configs')
