import json
import logging

from django.conf import settings
from ldap3 import Server, ALL, SIMPLE, Connection, SUBTREE, ALL_ATTRIBUTES
from ldap3.utils.conv import escape_filter_chars

from accounts.models import UserConnection

log = logging.getLogger(__name__)


def sync_accounts():
    server = Server(settings.LDAP_URL, get_info=ALL)
    conn = Connection(
        server,
        user=settings.LDAP_BIND_DN,
        password=settings.LDAP_PASSWORD,
        authentication=SIMPLE,
        auto_bind=True,
    )
    for userconnection in UserConnection.objects.all():
        conn.search(
            search_base=settings.LDAP_BASE_DN,
            search_scope=SUBTREE,
            search_filter="(entryUUID={uuid})".format(uuid=escape_filter_chars(str(userconnection.directory_key))),
            attributes=ALL_ATTRIBUTES,
        )
        # Convert the result to a list of dicts
        entries = [json.loads(entry.entry_to_json()) for entry in conn.entries]
        userconnection.latest_ldap_directory_data = entries
        userconnection.save()

