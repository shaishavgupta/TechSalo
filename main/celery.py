from __future__ import absolute_import, unicode_literals 
import os 
from celery import Celery 
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings') 
app = Celery('main')

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')   

app.conf.beat_schedule = {
    'send_notification_every_minute': {
        'task': 'salo.tasks.send_notification',
        'schedule': crontab(minute='*/1'),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))