#!/usr/bin/env bash
set +eux

export ACTIVATE_DEBUG_MODE=active

set -o allexport; source .env; set +o allexport
COMPOSE="$COMPOSE -f docker-compose.yml -f docker-compose.debug.yml"
. ./secrets.env
$COMPOSE up opa db -d
# Listen on 0.0.0.0 to allow access from inside docker container to this python instance.
(cd src; pipenv run ./manage.py $*)

