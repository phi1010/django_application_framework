import json
import logging
import time

from doors.mqtt_dynsec import admin_mqtt
from doors.models import Door, RemoteClient

log = logging.getLogger(__name__)


def update_mqtt_dynamic_security(sync=False):
    for rclient in RemoteClient.objects.all():
        update_mqtt_client(rclient, sync)


def update_mqtt_client(rclient, sync=False):
    log.info(f"updating mqtt client {rclient.id!r}")
    pub = admin_mqtt.set_client(
        username=rclient.username, password=rclient.token,
        allow_mqtt_ids=[door.mqtt_id for door in rclient.doors.all()],
        sync=sync
    )
