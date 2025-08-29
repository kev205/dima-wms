#!/bin/bash
set -e

gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --access-logfile - --error-logfile - --log-level info cms.wsgi:application