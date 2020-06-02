from __future__ import absolute_import, unicode_literals

import os
import sys


from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from fundoonotes.tasks import send_reminder

sys.path.append(os.path.abspath('FUNDOONOTES'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FUNDOONOTES.settings')
app = Celery('FUNDOONOTES')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(6.0, add.s(1,3), name='add every 10')
    # sender.add_periodic_task(5.0, add.s(1,100), name='add 5sec')
    sender.add_periodic_task(15.0, send_reminder.s(), name='send_reminder 15sec')
