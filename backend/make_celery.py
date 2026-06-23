from app import app
from celery_app import celery_init_app

celery = app.extensions["celery"]
