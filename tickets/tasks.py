from celery.schedules import crontab
from celery import shared_task
from .views import archieve_requests


@shared_task 
def archieving_task():
    archieve_requests()


@shared_task
def test():
    print("Testing Celery")