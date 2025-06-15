#!/bin/bash

# Navigate to the directory containing manage.py
cd "$(dirname "$0")/chakshu" || exit

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn chakshu.wsgi:application -b 0.0.0.0:8000
