from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings  # noqa

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings")
app.conf.broker_url = os.environ.get("BROKER_URL")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {}
