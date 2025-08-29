import logging

from django.core.management.base import BaseCommand

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Does something"

    def handle(self, *args, **options):
        log.info("some_task command called")
        pass  # TODO
