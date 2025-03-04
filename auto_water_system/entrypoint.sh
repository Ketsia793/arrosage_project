#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django application..."
exec python manage.py runserver 0.0.0.0:8000