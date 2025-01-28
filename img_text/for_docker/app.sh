#!/bin/bash

sleep 30
python manage.py makemigrations
python manage.py migrate
python manage.py shell < /src/for_docker/create_superuser.py &&
python manage.py runserver 0.0.0.0:8000