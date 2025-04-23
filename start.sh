#!/bin/sh

echo "Applying database migrations..."
uv run manage.py makemigrations
uv run manage.py migrate

echo "Starting Django server..."
uv run manage.py runserver 0.0.0.0:8000
