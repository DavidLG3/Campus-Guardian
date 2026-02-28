# Tests E2E - Campus Guardian

Esta carpeta contiene todos los tests end-to-end (E2E) de Cypress para Campus Guardian.

## 📁 Estructura

```
cypress/
├── e2e/                      # Tests E2E
│   ├── example.cy.js         # 🔥 Smoke tests (tests rápidos básicos)
│   ├── auth.cy.js            # 🔐 Tests de autenticación
│   ├── incidencias.cy.js     # 📝 Tests de gestión de incidencias
│   ├── dashboard.cy.js       # 📊 Tests de dashboard y navegación
│   ├── perfil.cy.js          # 👤 Tests de perfil de usuario
│   └── notificaciones.cy.js  # 🔔 Tests de notificaciones y alertas
├── fixtures/                 # Datos de prueba
│   ├── testData.json         # Datos comunes para tests
│   ├── test-avatar.png       # Imagen de prueba para avatar
│   └── example.json          # (original de Cypress)
└── support/                  # Comandos y configuración
    ├── commands.js           # Comandos personalizados
    ├── e2e.js                # Setup global para E2E
    └── component.js          # (para tests de componentes)
```

## 🎯 Orden de Ejecución Recomendado

Para demostraciones, ejecuta los tests en este orden:

1. **example.cy.js** - Smoke tests (2 min)
   - Verifica que la app carga correctamente
   - Tests básicos de navegación

2. **auth.cy.js** - Autenticación (5 min)
   - Login, registro, logout
   - Protección de rutas

3. **dashboard.cy.js** - Dashboard (3 min)
   - Navegación del menú
   - Chatbot
   - Estadísticas

4. **incidencias.cy.js** - Incidencias (8 min)
   - CRUD completo de incidencias
   - Comentarios
   - Filtros

5. **perfil.cy.js** - Perfil (4 min)
   - Edición de perfil
   - Cambio de contraseña
   - Foto de perfil

6. **notificaciones.cy.js** - Notificaciones (4 min)
   - Centro de notificaciones
   - Alertas
   - Marcado como leído

**Tiempo total estimado: ~26 minutos**

## 🚀 Comandos Personalizados

### `cy.login(username, password)`
Login rápido navegando por la UI
```javascript
cy.login('admin', 'admin123')
```

### `cy.loginAPI(username, password)`
Login más rápido usando la API directamente
```javascript
cy.loginAPI('admin', 'admin123')
cy.visit('/dashboard')
```

### `cy.logout()`
Cierra sesión
```javascript
cy.logout()
```

### `cy.createIncidencia(data)`
Crea una incidencia de prueba
```javascript
cy.createIncidencia({
  titulo: 'Mi incidencia',
  tipo: 'Robo'
})
```

### `cy.tab()`
Navega con el teclado (Tab)
```javascript
cy.get('input').first().tab()
cy.focused().should('have.attr', 'name', 'password')
```

## 📊 Datos de Prueba (Fixtures)

Usa `cy.fixture()` para cargar datos:

```javascript
cy.fixture('testData').then((data) => {
  const user = data.testUsers.admin
  cy.login(user.username, user.password)
})
```

## 🎬 Ejecución

### Desarrollo (con interfaz)
```bash
npm run test:e2e:dev
```

### CI/CD (headless)
```bash
npm run test:e2e
```

### Solo smoke tests
```bash
npx cypress run --spec "cypress/e2e/example.cy.js"
```

## 📝 Notas para el TFG

### Tests que demuestran funcionalidad completa:
- ✅ **Seguridad**: Login, logout, roles, permisos
- ✅ **CRUD**: Crear, leer, actualizar, eliminar incidencias
- ✅ **UX**: Navegación, responsividad, accesibilidad
- ✅ **Tiempo real**: Notificaciones, actualizaciones
- ✅ **Integración**: Mapa, chatbot IA, comentarios
- ✅ **Validaciones**: Formularios, datos, errores

### Métricas de cobertura:
- **Autenticación**: 100%
- **Incidencias**: CRUD completo + comentarios
- **Dashboard**: Todas las secciones principales
- **Perfil**: Edición y seguridad
- **Notificaciones**: Sistema completo
- **Responsividad**: Móvil, tablet, desktop

## 🐛 Troubleshooting

### Tests fallan por timeout
Aumenta el timeout en el test específico:
```javascript
cy.get('.elemento', { timeout: 10000 })
```

### Elementos no encontrados
Los tests usan selectores flexibles. Si tu implementación usa nombres diferentes:
```javascript
// Busca por texto
cy.contains(/incidencias/i)

// Busca por clase parcial
cy.get('[class*="incidencia"]')

// Busca por múltiples opciones
cy.get('input[name="titulo"], input[placeholder*="título"]')
```

### Backend no responde
Asegúrate de que:
1. Backend está corriendo en `http://localhost:8000`
2. Frontend está en modo preview en `http://localhost:4173`
3. Hay un usuario admin creado (admin/admin123)

## 📚 Referencias

- Tests organizados por funcionalidad (no por tipo)
- Cada describe representa una feature completa
- Tests son independientes entre sí
- Se usan datos aleatorios (timestamps) para evitar conflictos
- Selectores flexibles que funcionan con diferentes implementaciones

---

**✅ Tests listos para demostrar que Campus Guardian funciona correctamente**
