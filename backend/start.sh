#!/bin/sh

# May want to remove this at some point.. 
# not sure what it means when the database wipes clean if this is related or not
echo "Applying database migrations..."
uv run manage.py makemigrations
uv run manage.py migrate

echo "Starting Django server..."
uv run manage.py runserver 0.0.0.0:8000
