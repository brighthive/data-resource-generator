#!/bin/bash

gunicorn -b 0.0.0.0:8081 -w 1 wsgi:app --worker-class gevent --log-level debug
