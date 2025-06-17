from django.core.management.base import BaseCommand
from accounts import ldap

class Command(BaseCommand):
    help = "Synchronizes django accounts with the LDAP database"

    def handle(self, *args, **options):
        ldap.sync_accounts()

