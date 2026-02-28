# Tests E2E con Cypress - Campus Guardian

## 📋 Descripción

Tests automatizados end-to-end para la aplicación Campus Guardian usando Cypress. Los tests cubren las funcionalidades principales de autenticación, gestión de incidencias, navegación y flujos completos de usuario.

## ✅ Tests Actualizados

### 1. **auth.cy.js** - Autenticación
- ✅ Verificación de página de login
- ✅ Validación de credenciales incorrectas
- ✅ Login exitoso como ciudadano
- ✅ Login exitoso como admin (redirige a /admin)
- ✅ Logout correcto
- ✅ Protección de rutas después de logout

### 2. **incidencias.cy.js** - Gestión de Incidencias
- ✅ Visualización del listado de incidencias
- ✅ Visualización de "Mis Incidencias"
- ✅ Visualización del mapa con Leaflet
- ✅ Acceso al formulario de nueva incidencia
- ✅ Creación de incidencia usando el mapa interactivo
- ✅ Validación de campos requeridos
- ✅ Botón de ubicación actual

### 3. **dashboard.cy.js** - Dashboard y Navegación
- ✅ Carga del dashboard principal
- ✅ Visualización de estadísticas
- ✅ Menú hamburguesa (abrir/cerrar)
- ✅ Navegación entre secciones (Mapa, Incidencias, Mis Incidencias)
- ✅ Información del usuario en el menú
- ✅ Acceso al perfil
- ✅ Opciones especiales para Admin

### 4. **flujo-principal.cy.js** - Flujo E2E Completo
Simula el flujo completo de la aplicación:
- ✅ **Flujo Ciudadano**: Login → Crear incidencia → Ver mis incidencias → Mapa → Logout
- ✅ **Flujo Admin**: Login → Ver incidencias → Ver detalle → Mapa → Logout
- ✅ **Flujo Operador**: Login → Ver incidencias → Abrir detalle → Mapa → Logout
- ✅ **Verificación final**: Dashboard y consulta de estado

## 🔧 Configuración

### Usuarios de Prueba

Los tests usan usuarios configurados en `cypress/fixtures/testData.json`:

```json
{
  "testUsers": {
    "ciudadano": {
      "email": "test_ciudadano@campusguardian.test",
      "password": "Ciudadano123!",
      "tipo": "normal"
    },
    "operador": {
      "email": "test_operador@campusguardian.test",
      "password": "Operador123!",
      "tipo": "seguridad"
    },
    "admin": {
      "email": "test_admin@campusguardian.test",
      "password": "Admin123!",
      "tipo": "admin"
    }
  }
}
```

**⚠️ IMPORTANTE**: Estos usuarios deben existir en tu base de datos antes de ejecutar los tests.

### Crear Usuarios de Prueba

Ejecuta el script de creación de usuarios:

```bash
cd frontend/cypress
chmod +x crear-usuarios-test.sh
./crear-usuarios-test.sh
```

O créalos manualmente en tu base de datos Django.

## 🚀 Ejecución de Tests

### Modo Interactivo (recomendado para desarrollo)

```bash
cd frontend
npm run cypress:open
```

Luego selecciona el test que quieres ejecutar.

### Modo Headless (para CI/CD)

```bash
# Ejecutar todos los tests
npm run cypress:run

# Ejecutar un test específico
npx cypress run --spec "cypress/e2e/auth.cy.js"
```

### Ejecutar tests por categoría

```bash
# Solo autenticación
npx cypress run --spec "cypress/e2e/auth.cy.js"

# Solo incidencias
npx cypress run --spec "cypress/e2e/incidencias.cy.js"

# Solo dashboard
npx cypress run --spec "cypress/e2e/dashboard.cy.js"

# Flujo completo E2E
npx cypress run --spec "cypress/e2e/flujo-principal.cy.js"
```

## 📝 Comandos Personalizados

### `cy.login(email, password)`
Login rápido usando el formulario:
```javascript
cy.login('test_ciudadano@campusguardian.test', 'Ciudadano123!')
```

### `cy.logout()`
Cierra sesión usando el menú hamburguesa:
```javascript
cy.logout()
```

### `cy.createIncidencia(data)`
Crea una incidencia usando el mapa (EXPERIMENTAL):
```javascript
cy.createIncidencia({
  tipo: 'robo',
  descripcion: 'Test de robo',
  direccion: 'Biblioteca'
})
```

## 🔍 Adaptaciones Realizadas

Los tests han sido actualizados para reflejar la estructura actual de la aplicación:

1. **Splash Screen**: Se espera 3 segundos para que termine el splash
2. **Login**: Usa campos `#email` y `#password`
3. **Redirecciones**: Admin → `/admin`, Ciudadano → `/dashboard`
4. **Menú Hamburguesa**: Requiere clic en `.hamburger-btn` y `.menu-close-btn`
5. **Formulario de Incidencias**: 
   - Ya NO usa campo "título"
   - Usa selección en mapa interactivo (#incidencia-map)
   - Campos: `#tipo`, `#descripcion`, `#direccion`
6. **Mapa**: Se valida `.leaflet-container` y `.leaflet-control-zoom`
7. **Logout**: Requiere abrir menú y hacer clic en "Cerrar Sesión"

## ⚙️ Requisitos Previos

1. **Backend corriendo**: `python manage.py runserver`
2. **Frontend corriendo**: `npm run dev`
3. **Usuarios de prueba creados** en la base de datos
4. **Base de datos limpia** o con datos de prueba controlados

## 📊 Cobertura de Tests

- ✅ Autenticación (Login/Logout)
- ✅ Protección de rutas
- ✅ Navegación entre vistas
- ✅ Creación de incidencias
- ✅ Visualización de mapas (Leaflet)
- ✅ Listados de incidencias
- ✅ Roles de usuario (Ciudadano, Operador, Admin)
- ✅ Flujos E2E completos

## 🐛 Solución de Problemas

### Los tests fallan en login
- Verifica que los usuarios de prueba existen en la BD
- Comprueba que el backend está corriendo en `localhost:8000`
- Revisa las credenciales en `testData.json`

### Los tests del mapa fallan
- Asegúrate de que Leaflet está cargando correctamente
- Aumenta los timeouts si la conexión es lenta
- Verifica que hay incidencias en la base de datos

### Los tests no encuentran elementos
- Usa `cy.get().debug()` para inspeccionar el DOM
- Verifica los selectores en el código fuente de la app
- Aumenta los `cy.wait()` si es necesario

## 📚 Recursos

- [Documentación Cypress](https://docs.cypress.io)
- [Cypress Best Practices](https://docs.cypress.io/guides/references/best-practices)
- [Cypress API](https://docs.cypress.io/api/table-of-contents)

## 🎯 Próximos Tests a Implementar

- [ ] Tests de comentarios en incidencias
- [ ] Tests de cambio de estado
- [ ] Tests de asignación de incidencias
- [ ] Tests de notificaciones
- [ ] Tests de alertas
- [ ] Tests de perfil de usuario
- [ ] Tests de gestión de usuarios (Admin)
- [ ] Tests de carga de archivos/multimedia
- [ ] Tests de chatbot Guardian

---

**Última actualización**: 27 de febrero de 2026
**Versión**: 2.0 - Adaptada a la aplicación actual
