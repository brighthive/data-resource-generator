#!/bin/bash

gunicorn -b 0.0.0.0:8081 --workers=1 --threads=4 wsgi:app --log-level debug
