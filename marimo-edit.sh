#!/bin/bash
set -eux
export ACTIVATE_DEBUG_MODE=active
set -o allexport; source .env; set +o allexport
COMPOSE="$COMPOSE -f docker-compose.yml -f docker-compose.debug.yml"
. ./secrets.env
$COMPOSE up opa db prometheus grafana loki alloy &
sleep 1
marimo edit