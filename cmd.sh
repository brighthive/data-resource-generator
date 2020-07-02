#!/bin/bash

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -w 4 -b 0.0.0.0:8081 wsgi:app --reload --worker-class gevent --timeout 600  # nosec
else
  sleep 10
  gunicorn -b 0.0.0.0:8081 -w 1 wsgi:app --worker-class gevent
fi
