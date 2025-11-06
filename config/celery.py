# config/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# create Celery app
app = Celery('config')

# read config from Django settings, using CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks from all installed apps
app.autodiscover_tasks()

# example beat schedule (hourly anomaly detection)
app.conf.beat_schedule = {
    'detect_suspicious_ips_hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': 3600.0,  # every 1 hour
    },
}

# optional: debug info
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
