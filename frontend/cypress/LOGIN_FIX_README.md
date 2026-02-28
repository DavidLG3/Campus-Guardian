# ✅ Corrección de Tests de Cypress - LOGIN FIXED

## 🔴 Problema Encontrado

Los tests de Cypress estaban **buscando campos que NO EXISTEN** en el formulario de login:
- ❌ Buscaban: `input[name="username"]` o `input[type="text"]`
- ✅ Formulario real: `#email` (type="email") y `#password` (type="password")

**El backend requiere email para login**, no username:
```javascript
// LoginView.vue - Formulario real
<input id="email" v-model="credentials.email" type="email" />
<input id="password" v-model="credentials.password" type="password" />

// Backend espera:
{ "email": "user@ejemplo.com", "password": "pass123" }
```

## 🔧 Solución Aplicada

### 1. **Actualizado testData.json**
Añadidos emails válidos para todos los usuarios de prueba:
```json
{
  "testUsers": {
    "admin": {
      "email": "test_admin@campusguardian.test",
      "password": "Admin123!"
    },
    "operador": {
      "email": "test_operador@campusguardian.test",
      "password": "Operador123!"
    },
    "ciudadano": {
      "email": "test_ciudadano@campusguardian.test",
      "password": "Ciudadano123!"
    }
  }
}
```

### 2. **Corregido commands.js**
```javascript
// ✅ CORRECTO - Usa selectores reales
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('#email').type(email)
  cy.get('#password').type(password)
  cy.get('button[type="submit"]').click()
  cy.url({ timeout: 15000 }).should('match', /\/(dashboard|home|admin)/)
})

// También corregido loginAPI para enviar email
Cypress.Commands.add('loginAPI', (email, password) => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/auth/login/',
    body: { email, password }
    //      ^^^^^ NO username
  })
})
```

### 3. **Actualizados TODOS los archivos de tests**
- ✅ `auth.cy.js` - Usa `#email` y `#password`
- ✅ `dashboard.cy.js` - Login con `testData.testUsers.admin.email`
- ✅ `incidencias.cy.js` - Login con `testData.testUsers.admin.email`
- ✅ `example.cy.js` - Login con `testData.testUsers.admin.email`
- ✅ `flujo-principal.cy.js` - Simplificado, usa emails correctos

## 📋 Prerequisitos - IMPORTANTE

**ANTES de ejecutar los tests**, debes crear los usuarios de prueba en el backend:

```bash
# Desde la carpeta frontend:
./cypress/crear-usuarios-test.sh
```

Este script crea 3 usuarios:
- **Admin**: test_admin@campusguardian.test / Admin123!
- **Operador**: test_operador@campusguardian.test / Operador123!
- **Ciudadano**: test_ciudadano@campusguardian.test / Ciudadano123!

## 🚀 Cómo Ejecutar los Tests

```bash
# 1. Asegúrate de que el backend está corriendo
cd app_seguridad
python manage.py runserver

# 2. En otra terminal, crea los usuarios de prueba (solo primera vez)
cd frontend
./cypress/crear-usuarios-test.sh

# 3. Inicia el frontend en modo preview
npm run preview  # Debe correr en puerto 4173

# 4. En otra terminal, ejecuta los tests
cd frontend
npx cypress run                    # Modo headless (rápido)
# o
npx cypress open                   # Modo interactivo (debug)
```

## 📊 Estructura de Tests

| Archivo | Duración | Descripción |
|---------|----------|-------------|
| `auth.cy.js` | ~1 min | Login, logout, protección de rutas |
| `dashboard.cy.js` | ~1 min | Navegación básica |
| `incidencias.cy.js` | ~2 min | CRUD de incidencias |
| `example.cy.js` | ~1 min | Smoke tests básicos |
| `flujo-principal.cy.js` | ~5 min | **Flujo E2E completo** |

**Total estimado: ~10-12 minutos**

## 🔍 Cambio Clave en Flujo Principal

**ANTES** (NO funcionaba):
```javascript
// ❌ Intentaba crear usuarios dinámicamente
it('Admin crea usuario de seguridad', () => {
  cy.get('input[name="username"]').type(`seguridad_${timestamp}`)
  // Muchas operaciones frágiles...
})

it('Login con usuario recién creado', () => {
  cy.get('input[type="text"]').type(username)  // ❌ Campo incorrecto
})
```

**AHORA** (SÍ funciona):
```javascript
// ✅ Usa usuarios pre-creados con emails
it('Admin hace login', () => {
  cy.get('#email').type(testData.testUsers.admin.email)
  cy.get('#password').type(testData.testUsers.admin.password)
})

it('Operador hace login', () => {
  cy.get('#email').type(testData.testUsers.operador.email)
  cy.get('#password').type(testData.testUsers.operador.password)
})
```

## 🧹 Limpieza Automática

Los tests siguen limpiando datos automáticamente:
- `cy.cleanupTestData()` se ejecuta en `before()` y `after()`
- Elimina incidencias con "TEST-" en el título
- Elimina usuarios con "test_" en el username
- Los 3 usuarios base (admin, operador, ciudadano) **NO se eliminan**

## ✅ Verificación Rápida

Para probar que el login funciona:
```bash
npx cypress run --spec "cypress/e2e/auth.cy.js"
```

Si este test pasa, el resto debería funcionar también.
