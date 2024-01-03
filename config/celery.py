from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kathmandu')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()