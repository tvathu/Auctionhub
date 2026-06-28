import os
from celery import Celery

# Tell Celery which Django settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_site.settings')

app = Celery('auction_site')

# Read Celery config from Django settings (keys starting with CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py files in all installed apps
app.autodiscover_tasks()