from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "flywatch.settings")
app = Celery("flywatch")

app.config_from_object("django.conf:settings", namespace="CELERY")

