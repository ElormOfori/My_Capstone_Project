import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_Capstone_Project.settings')

app = Celery('My_Capstone_Project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
