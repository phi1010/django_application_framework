# Readme

This is an example for a django application packaged in a docker container.

This was stripped down from https://github.com/zam-haus/door_commander/commit/b107fbae711e0bca8db5edd21766f0416e080408

Add the host to ALLOWED_HOSTS in .env file

sudo apt install podman podman-compose python3-pip pipenv

pipenv install
pipenv shell
(cd src ; ./manage.py makemigrations)
./set-secrets.sh
./launch-containers.sh
