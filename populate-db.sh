#!/bin/sh

echo ">>> create db"
docker-compose run django python manage.py migrate

echo ">>> load root user"
docker-compose run django python manage.py loaddata fixtures/users.json

echo ">>> load test data"
docker-compose run django python manage.py loaddata current/fixtures/current.json