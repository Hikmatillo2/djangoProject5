#!/bin/bash

service nginx start
# service posgresql start
/bin/python3 awaiter.py
if [ ! -f "/srv/djangoProject5/flag" ]; then
    python3 manage.py collectstatic --noinput --settings settings.development
    python3 manage.py migrate --settings settings.development && sleep 1
    python3 manage.py makemigrations --settings settings.development && sleep 1
    python3 manage.py migrate --settings settings.development && sleep 1
    python3 manage.py initadmin --settings settings.development
    echo 1 > /srv/djangoProject5/flag
fi

/bin/gunicorn3 wsgi:application -b 127.0.0.1:8000 --env DJANGO_SETTINGS_MODULE=settings.development --user www-data --group www-data
