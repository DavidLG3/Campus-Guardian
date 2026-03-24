#!/bin/bash

# Script para preparar y verificar el entorno de tests de Cypress
# Campus Guardian - TFG

echo "🎓 Campus Guardian - Preparación de Tests E2E"
echo "=============================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar si un puerto está en uso
port_in_use() {
    lsof -i:"$1" >/dev/null 2>&1
}

echo "📋 Verificando dependencias..."
echo ""

# Verificar Node.js
if command_exists node; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓${NC} Node.js instalado: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js no está instalado"
    exit 1
fi

# Verificar npm
if command_exists npm; then
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✓${NC} npm instalado: $NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm no está instalado"
    exit 1
fi

# Verificar Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python instalado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python no está instalado"
    exit 1
fi

echo ""
echo "🔍 Verificando servicios..."
echo ""

# Verificar si el backend está corriendo (puerto 8000)
if port_in_use 8000; then
    echo -e "${GREEN}✓${NC} Backend corriendo en http://localhost:8000"
else
    echo -e "${YELLOW}⚠${NC} Backend NO está corriendo en puerto 8000"
    echo "   Ejecuta: cd app_seguridad && python manage.py runserver"
fi

# Verificar si el frontend está en preview (puerto 4173)
if port_in_use 4173; then
    echo -e "${GREEN}✓${NC} Frontend preview corriendo en http://localhost:4173"
else
    echo -e "${YELLOW}⚠${NC} Frontend preview NO está corriendo en puerto 4173"
    echo "   Ejecuta: cd frontend && npm run build && npm run preview"
fi

echo ""
echo "📦 Verificando instalación de Cypress..."
echo ""

cd "$(dirname "$0")/.." || exit

# Verificar si node_modules existe
if [ -d "node_modules" ]; then
    echo -e "${GREEN}✓${NC} node_modules existe"
else
    echo -e "${YELLOW}⚠${NC} node_modules no existe. Instalando dependencias..."
    npm install
fi

# Verificar si Cypress está instalado
if [ -d "node_modules/cypress" ]; then
    CYPRESS_VERSION=$(npx cypress version 2>/dev/null | grep "Cypress package version" | cut -d: -f2 | xargs)
    echo -e "${GREEN}✓${NC} Cypress instalado: $CYPRESS_VERSION"
else
    echo -e "${RED}✗${NC} Cypress no está instalado"
    echo "   Ejecuta: npm install"
    exit 1
fi

echo ""
echo "🗂️  Verificando archivos de test..."
echo ""

# Verificar que los archivos de test existen
TEST_FILES=(
    "cypress/e2e/example.cy.js"
    "cypress/e2e/auth.cy.js"
    "cypress/e2e/incidencias.cy.js"
    "cypress/e2e/dashboard.cy.js"
    "cypress/e2e/perfil.cy.js"
    "cypress/e2e/notificaciones.cy.js"
)

for file in "${TEST_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file no encontrado"
    fi
done

echo ""
echo "🔧 Verificando fixtures..."
echo ""

if [ -f "cypress/fixtures/testData.json" ]; then
    echo -e "${GREEN}✓${NC} testData.json"
else
    echo -e "${YELLOW}⚠${NC} testData.json no encontrado"
fi

if [ -f "cypress/fixtures/test-avatar.png" ]; then
    echo -e "${GREEN}✓${NC} test-avatar.png"
else
    echo -e "${YELLOW}⚠${NC} test-avatar.png no encontrado"
fi

echo ""
echo "🎯 Verificando configuración..."
echo ""

if [ -f "cypress.config.js" ]; then
    echo -e "${GREEN}✓${NC} cypress.config.js existe"
else
    echo -e "${RED}✗${NC} cypress.config.js no encontrado"
fi

echo ""
echo "=============================================="
echo ""

# Verificar si todo está listo
if port_in_use 8000 && port_in_use 4173; then
    echo -e "${GREEN}✅ ¡Todo listo para ejecutar los tests!${NC}"
    echo ""
    echo "Comandos disponibles:"
    echo "  npm run test:e2e:dev    # Abrir Cypress UI"
    echo "  npm run test:e2e        # Ejecutar tests en headless"
    echo ""
    echo "¿Quieres abrir Cypress ahora? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        npm run test:e2e:dev
    fi
else
    echo -e "${YELLOW}⚠ Falta iniciar algunos servicios${NC}"
    echo ""
    echo "Pasos para preparar el entorno:"
    echo ""
    if ! port_in_use 8000; then
        echo "1. Iniciar backend:"
        echo "   cd app_seguridad"
        echo "   python manage.py runserver"
        echo ""
    fi
    if ! port_in_use 4173; then
        echo "2. Iniciar frontend preview:"
        echo "   cd frontend"
        echo "   npm run build"
        echo "   npm run preview"
        echo ""
    fi
    echo "3. Ejecutar este script nuevamente:"
    echo "   ./cypress-setup.sh"
fi

echo ""
echo "📚 Para más información, consulta:"
echo "   - frontend/CYPRESS_TESTS.md"
echo "   - frontend/cypress/README.md"
echo ""
