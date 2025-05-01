#!/bin/sh

set -a
source ./.env
set +a

echo "Updating packages..."
uv sync --frozen

echo "Applying database migrations..."
uv run manage.py makemigrations
uv run manage.py migrate

echo "Collecting static files..."
uv run manage.py collectstatic --no-input


echo "Starting Gunicorn WSGI server..."
uv run gunicorn final.wsgi --bind 127.0.0.1:8000 --workers 8 --threads 4 &


echo "Starting nginx..."
nginx -g "daemon off;"
