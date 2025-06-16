# "$CONTROL/dynamic-security/v1/response
"""
[
{
  "responses": [
    {
      "command": "getRole",
      "data": {
        "role": {
          "rolename": "admin",
          "acls": [
            {
              "acltype": "publishClientSend",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientSend",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "$SYS/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "publishClientReceive",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "$CONTROL/dynamic-security/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "$SYS/#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "subscribePattern",
              "topic": "#",
              "priority": 0,
              "allow": true
            },
            {
              "acltype": "unsubscribePattern",
              "topic": "#",
              "priority": 0,
              "allow": true
            }
          ]
        }
      }
    }
  ]
},
{"responses":[{"command":"listRoles","data":{"totalCount":1,"roles":["admin"]}}]}


]
"""

import json
import threading
import time
from dataclasses import dataclass, field
from json import loads
import logging
from numbers import Number

from decorated_paho_mqtt import GenericMqttEndpoint, pack_topic
from django.conf import settings
from django.utils.functional import lazy
from icecream import ic
from paho.mqtt.client import MQTTMessage
from pymaybe import maybe

from django.conf import settings
from doors.models import Door
import lazy_object_proxy

MQTT_CLIENT_KWARGS = settings.MQTT_CLIENT_KWARGS
MQTT_SERVER_KWARGS = settings.MQTT_SERVER_KWARGS
MQTT_PASSWORD_AUTH = settings.MQTT_PASSWORD_AUTH
MQTT_TLS = settings.MQTT_TLS

log = logging.getLogger(__name__)


@dataclass
class SetUserTask:
    username: str
    password: str
    roles: list[str]


@dataclass
class DynSecAcl:
    acltype: str
    """
    Where acltype is one of 
        publishClientSend, publishClientReceive,
        subscribeLiteral, subscribePattern,
        unsubscribeLiteral, and unsubscribePattern.
    """
    topic: str
    priority: int = field(default=0)
    allow: bool = field(default=True)


@dataclass
class SetRolesTask:
    username: str
    password: str
    acls: list[DynSecAcl]


def prepare_acls(mqtt_id) -> list[DynSecAcl]:
    return [
        DynSecAcl(acltype="subscribePattern", topic=pack_topic("door/+/", mqtt_id) + "#", ),
        DynSecAcl(acltype="publishClientSend", topic=pack_topic("door/+/presence", mqtt_id), ),
        DynSecAcl(acltype="publishClientSend", topic=pack_topic("door/+/open/confirm", mqtt_id), ),
        DynSecAcl(acltype="publishClientSend", topic=pack_topic("locator/+/", mqtt_id) + "#", ),
    ]


class MqttAdminEndpoint(GenericMqttEndpoint):
    def __init__(self, client_kwargs: dict, password_auth: dict, server_kwargs: dict, tls: bool):
        super().__init__(client_kwargs, password_auth, server_kwargs, tls)
        self._cv = threading.Condition()

    @property
    def is_connected(self):
        """This is only informational, please use qos=1 or qos=2 if you require a message to be sent."""
        return self._mqttc.is_connected()

    @GenericMqttEndpoint.subscribe_decorator("$CONTROL/dynamic-security/v1/response", qos=2)
    def admin_response(self, *, client, userdata, message: MQTTMessage):
        try:
            with self._cv:
                # ic(message)
                # ic(message.payload)
                data = loads(message.payload)
                match data:
                    case {"responses": commands}:
                        for command in commands:
                            self._cv.notify_all()
                            match command:
                                case {"command": command_name, "error": error}:
                                    log.warning(f"Error executing command {command_name!r}: {error!r}")
                                case {"command": command_name}:
                                    log.debug(f"Executed command {command_name!r}")
                                case {"command": command_name, "data": data}:
                                    log.debug(f"Executed command {command_name!r}, returned data {data}")
        except Exception as e:
            log.error(f"Failed to parse message: {e}")

    def set_client(self, username, password, allow_mqtt_ids, sync=False):
        if not wait_until(lambda :self.is_connected, timeout=5):
            raise Exception("Not connected to MQTT server")

        with self._cv:
            payload = dict(
                commands=
                [
                    dict(
                        command="createRole",
                        rolename=mqtt_id,
                        textname=mqtt_id,
                        acls=[acl.__dict__ for acl in prepare_acls(mqtt_id)]
                    )
                    for mqtt_id in allow_mqtt_ids
                ] + [
                    dict(
                        command="modifyRole",
                        rolename=mqtt_id,
                        textname=mqtt_id,
                        acls=[acl.__dict__ for acl in prepare_acls(mqtt_id)]
                    )
                    for mqtt_id in allow_mqtt_ids
                ]+[
                    dict(
                        command="createClient",
                        username=username,
                        password=password,
                        textname=username,
                        roles=[dict(rolename=mqtt_id, priority=0) for mqtt_id in allow_mqtt_ids],
                    ),
                    dict(
                        command="modifyClient",
                        username=username,
                        password=password,
                        textname=username,
                        roles=[dict(rolename=mqtt_id, priority=0) for mqtt_id in allow_mqtt_ids],
                    ),
                ])
            pub = self._mqttc.publish("$CONTROL/dynamic-security/v1", qos=2, retain=False, payload=json.dumps(payload))
            #pub.wait_for_publish()
            if sync:
                if not self._cv.wait(5):
                    raise Exception("Timed out waiting for MQTT response")



def start_connection():
    log.debug(f"Starting MQTT connection {MQTT_SERVER_KWARGS=}, {MQTT_CLIENT_KWARGS=}, {MQTT_TLS=}")
    door_commander_mqtt = MqttAdminEndpoint(
        client_kwargs=MQTT_CLIENT_KWARGS,
        password_auth=MQTT_PASSWORD_AUTH,
        server_kwargs=MQTT_SERVER_KWARGS,
        tls=MQTT_TLS
    )
    door_commander_mqtt.connect()
    return door_commander_mqtt


admin_mqtt: MqttAdminEndpoint = lazy_object_proxy.Proxy(start_connection)


def wait_until(condition, interval=0.1, timeout=1, *args):
    start = time.time()
    while not (result:=condition(*args)) and time.time() - start < timeout:
        time.sleep(interval)
    # True if condition fulfilled
    return result