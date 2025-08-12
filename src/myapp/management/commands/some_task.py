from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Does something"

    def handle(self, *args, **options):
        pass # TODO

