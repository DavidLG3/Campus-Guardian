#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ir al directorio del proyecto Django
cd app_seguridad

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

# Crear superusuario por defecto
python manage.py create_default_superuser

echo "Build completado exitosamente!"
