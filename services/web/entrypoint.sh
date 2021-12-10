#!/bin/bash

if [ "$DATABASE" = "POSTGIS" ]
then
    echo "Waiting for postgis..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Postgis started"
fi

python manage.py create_db

exec "$@"