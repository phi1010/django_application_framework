#!/bin/bash
set -ef -o pipefail
# set -x

set -o allexport; source .env; set +o allexport
COMPOSE="$COMPOSE -f docker-compose.yml -f docker-compose.prod.yml"

# stop and remove all containers, otherwise we can't pass the new parameters as environment variables
$COMPOSE down

# clear the file
touch secrets.env
. secrets.env

# helper function, uses 256bit of entropy
generate_password() { head -c32 /dev/random | base64; }




echo ::group::MQTT Django Password
if [[ ! $MQTT_PASSWD_CONTROLLER ]] ; then
  # generate all necessary secrets and save them
  MQTT_PASSWD_CONTROLLER="$(generate_password)"
  export MQTT_PASSWD_CONTROLLER
  declare -p MQTT_PASSWD_CONTROLLER >>secrets.env
  echo "Check mosquitto/config/mosquitto.passwd for duplicates!"
  touch mosquitto/config/mosquitto.passwd || true # otherwise a directory will be created
fi
$COMPOSE run --rm mqtt mosquitto_passwd -b /mosquitto/config/mosquitto.passwd controller "$MQTT_PASSWD_CONTROLLER"
echo ::endgroup::



echo ::group::pgSQL Superuser Password
if [[ ! $POSTGRES_PASSWORD ]] ; then
  POSTGRES_PASSWORD="$(generate_password)"
  export POSTGRES_PASSWORD
  declare -p POSTGRES_PASSWORD >>secrets.env
fi
$COMPOSE run --rm db /docker-postgres-run-command.sh /update_superuser.sh
echo ::endgroup::

echo ::group::pgSQL Django Password
if [[ ! $POSTGRES_PASSWORD_DJANGO ]] ; then
  POSTGRES_PASSWORD_DJANGO="$(generate_password)"
  export POSTGRES_PASSWORD_DJANGO
  declare -p POSTGRES_PASSWORD_DJANGO >>secrets.env
fi
USER="${POSTGRES_USER_DJANGO}" PASSWORD="${POSTGRES_PASSWORD_DJANGO}" DB="${POSTGRES_DB_DJANGO}" \
  $COMPOSE run --rm \
  -e USER -e PASSWORD -e DB \
  db /docker-postgres-run-command.sh /update_other_user.sh
echo ::endgroup::




echo ::group::OPA Bearer Token
if [[ ! $OPA_BEARER_TOKEN ]] ; then
  echo "Token used to connect the Django OPA client to the internal OPA server instance"
  OPA_BEARER_TOKEN="$(generate_password)"
  export OPA_BEARER_TOKEN
  declare -p OPA_BEARER_TOKEN >>secrets.env
fi
echo ::endgroup::

echo ::group::OPA Bundle Bearer Token
if [[ ! $OPA_BUNDLE_SERVER_BEARER_TOKEN ]] ; then
  echo "Token used to connect an OPA client instance to the Django bundle server"
  OPA_BUNDLE_SERVER_BEARER_TOKEN="$(generate_password)"
  export OPA_BUNDLE_SERVER_BEARER_TOKEN
  declare -p OPA_BUNDLE_SERVER_BEARER_TOKEN >>secrets.env
fi
echo ::endgroup::



if [[ ! $OIDC_RP_CLIENT_SECRET ]] ; then
  echo "TODO: You need to provide OIDC_RP_CLIENT_SECRET manually."
  OIDC_RP_CLIENT_SECRET=""
  export OIDC_RP_CLIENT_SECRET
  declare -p OIDC_RP_CLIENT_SECRET >> secrets.env
fi

echo "TODO: You need to provide LDAP_PASSWORD manually."
LDAP_PASSWORD="password"
export LDAP_PASSWORD
declare -p LDAP_PASSWORD >> secrets.env





echo "Secrets successfully set"
