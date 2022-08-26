#!/bin/bash

service nginx start
# service posgresql start
/bin/gunicorn3 wsgi:application -b 127.0.0.1:8000 --env DJANGO_SETTINGS_MODULE=settings.development --user www-data --group www-data
