import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home_accounting.settings')

app = Celery('home_accounting')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()