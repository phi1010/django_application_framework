from celery import shared_task
from django.core.management import call_command


@shared_task
def some_task():
    call_command("some_task", )