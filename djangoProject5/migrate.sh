#!/bin/bash

python3 manage.py collectstatic --noinput --settings settings.development
python3 manage.py migrate --settings settings.development && \
sleep 1 && python3 manage.py makemigrations --settings settings.development && sleep 1 && \
python3 manage.py migrate --settings settings.development && sleep 1 && \
python3 manage.py initadmin --settings settings.development
echo "" > /srv/djangoProject5/migrate.sh
