import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRF_Library.settings")

app = Celery("DRF_Library")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
