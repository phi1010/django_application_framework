#!/usr/bin/env bash
set +eux
echo "==== THIS REQUIRES debug.sh RUNNING IN PARALLEL ===="

set -o allexport; source .env; set +o allexport
COMPOSE="$COMPOSE -f docker-compose.yml -f docker-compose.debug.yml"
. ./secrets.env
$COMPOSE up opa-client-prototype

