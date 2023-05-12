#!/bin/bash

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations 
python manage.py migrate

gunicorn jobboard.wsgi:application --bind 0.0.0.0:$PORT --workers 4
