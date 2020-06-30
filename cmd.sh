#!/bin/bash

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -w 4 -b 0.0.0.0:8081 wsgi:app --reload --worker-class gevent --timeout 600
else
  pipenv run python wsgi.py
  # gunicorn -b 0.0.0.0:8081 -w 4 wsgi:app --worker-class gevent
fi
