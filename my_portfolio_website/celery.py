import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_portfolio_website.settings")
app = Celery("my_portfolio_website")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()