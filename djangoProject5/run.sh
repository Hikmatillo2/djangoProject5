#!/bin/bash

'''service nginx start
/srv/djangoProject5/migrate.sh
/bin/gunicorn3 wsgi:application -b 127.0.0.1:8000 --env DJANGO_SETTINGS_MODULE=settings.development --user www-data --group www-data'''
