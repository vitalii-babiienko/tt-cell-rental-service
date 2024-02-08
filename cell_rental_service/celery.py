import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cell_rental_service.settings")

app = Celery("cell_rental_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
