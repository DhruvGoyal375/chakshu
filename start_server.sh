#!/bin/bash

# Ensure the script runs from the project root directory (where the script is located)
cd "$(dirname "$0")" || exit

# Start Gunicorn server using poetry to ensure it runs in the correct virtual environment.
# The --chdir flag tells Gunicorn to change to the 'chakshu' directory before loading the app,
# which is necessary for it to find the 'chakshu.wsgi' module.
echo "Starting Gunicorn server..."
poetry run gunicorn --chdir chakshu chakshu.wsgi:application -b 0.0.0.0:8000 --workers 3 --timeout 1200
