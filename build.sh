#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Go to the Django project directory
cd app_seguridad

# Collect static files
python manage.py collectstatic --no-input

# Apply migrations
python manage.py migrate

# Create default superuser
python manage.py create_default_superuser

echo "Build completado exitosamente!"
