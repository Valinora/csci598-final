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


echo "Starting Django webserver..."
uv run manage.py runserver 0.0.0.0:8000
