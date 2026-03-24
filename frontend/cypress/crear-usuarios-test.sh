#!/bin/bash
# Script to create test users in the backend before running Cypress tests

echo "==================================="
echo "Creando usuarios de prueba..."
echo "==================================="

# Navigate to the backend directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../../app_seguridad"

if [ ! -f "$BACKEND_DIR/manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py en $BACKEND_DIR"
    exit 1
fi

cd "$BACKEND_DIR"

# Create test users using Django management command
python manage.py crear_usuarios_test

echo ""
echo "==================================="
echo "✓ Proceso completado"
echo "==================================="
echo ""
echo "Usuarios disponibles:"
echo "  - Admin: test_admin@uam.es / Admin123!"
echo "  - Operador: test_operador@uam.es / Operador123!"
echo "  - Ciudadano: test_ciudadano@estudiante.uam.es / Ciudadano123!"
echo ""
echo "Ahora puedes ejecutar los tests de Cypress:"
echo "  cd frontend && npm run test:e2e"
echo ""
