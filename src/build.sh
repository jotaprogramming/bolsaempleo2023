#!/usr/bin/env bash
# exit on error

set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations 
python manage.py migrate 
python manage.py collectstatic --no-input

# DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput