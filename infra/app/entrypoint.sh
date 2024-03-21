#!/bin/bash

python3 manage.py migrate
python3 manage.py collectstatic --no-input

gunicorn core.wsgi --bind 0:8000
