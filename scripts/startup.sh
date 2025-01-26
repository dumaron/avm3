#!/bin/sh
python manage.py migrate
gunicorn --bind :8000 --workers 1 avm3.wsgi & supercronic /code/crontab