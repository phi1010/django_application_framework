# Wichtiges zur Nutzung

./set-secrets.sh löscht secrets an lustigen Stellen - NICHT in einem schon konfigurierten Umfeld nutzen, sonst ist alles kaputt:

 * Türenzugangsdaten werden in der mosquitto.passwd gelöscht


# Alte "Readme"

0. Set your compose environment in .env (`docker compose` on Ubuntu, `docker-compose` on Debian, `podman-compose` if using Podman)
1. Add the hostname 
   1. in .env to ALLOWED_HOSTS
   2. in nginx.conf to server_name
2. ./set-secrets.sh
3. ./create-superuser.sh
4. ./launch-containers.sh
5. Login to http://127.0.0.1:80
6. Open the admin interface
7. Create a door
8. Start ./mqtt_dump_all_messages.sh in a separate terminal
9. Open the application home page
10. Click the button
11. Watch the listener receiving the mqtt message
12. You can update a door's status with the following command (fill in your door's mqtt id)

    ```(. secrets.env ; mosquitto_pub -h localhost -u controller -P "${MQTT_PASSWD_CONTROLLER}" -p 1883 -d -t 'door/f16f33d2-7d87-45d3-937d-f5d64d957e8f/presence' -m 'true')```

# Development with pycharm
You need to set some environment variables in the run configuration:

```
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=door_commander.settings;ACTIVATE_DEBUG_MODE=active;OPA_URL=http://localhost:8181/
```

See also the .env loaded by pipenv run and debug.sh

# OPA debugging
You can access the data in the debug-mode-containers started with debug.sh via 

http://127.0.0.1:8181/v1/data/app/door_commander/physical_access

or you can go to http://127.0.0.1:8181/ and use the query

```
result := data.app.door_commander.physical_access
```

Authentication for the OPA server is disabled in debug containers

The bundle server is available at http://127.0.0.1:8000/opa-bundles/bundles/sidecar_authz.tar.gz when running debug.sh.

The RPi OPA Instance started with ./debug-opa-client.sh while running ./debug.sh can be accessed via http://127.0.0.1:8182/v1/data .