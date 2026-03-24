# Campus Guardian 🛡️

**Sistema Integral de Gestión de Seguridad Universitaria**

*Trabajo de Fin de Grado - Ingeniería Informática*  
*Universidad Autónoma de Madrid (UAM)*  
*Curso 2025-2026*

---

## 📋 Tabla de Contenidos

- [Resumen Ejecutivo](#-resumen-ejecutivo)
- [Contexto y Motivación](#-contexto-y-motivación)
- [Objetivos del Proyecto](#-objetivos-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Modelos de Datos](#-modelos-de-datos)
- [Funcionalidades Principales](#-funcionalidades-principales)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Sistema de Testing](#-sistema-de-testing)
- [Decisiones de Diseño](#-decisiones-de-diseño)
- [APIs y Endpoints](#-apis-y-endpoints)
- [Seguridad](#-seguridad)
- [Despliegue](#-despliegue)
- [Trabajo Futuro](#-trabajo-futuro)

---

## 📝 Resumen Ejecutivo

**Campus Guardian** es una plataforma web completa diseñada para mejorar la seguridad y la capacidad de respuesta ante incidentes en entornos universitarios. El sistema permite a estudiantes, profesores y personal administrativo reportar incidencias de seguridad en tiempo real, mientras que el personal de seguridad y administradores pueden gestionar, rastrear y resolver estas incidencias de manera eficiente.

### Características Destacadas

- 🚨 **Reporte de Incidencias Geolocalizadas**: Sistema de mapas interactivos con Leaflet/OpenStreetMap
- 🤖 **Asistente Virtual con IA**: Chatbot integrado con Google Gemini API para ayuda contextual
- 👥 **Sistema de Roles Robusto**: Tres niveles de acceso (Ciudadano, Operador, Administrador)
- 📱 **Diseño Responsive**: Interfaz optimizada para dispositivos móviles y desktop
- 🔐 **Autenticación Segura**: JWT con refresh tokens y validaciones estrictas
- 📊 **Dashboard Analítico**: Visualización de estadísticas y métricas en tiempo real
- 💬 **Sistema de Comentarios**: Comunicación bidireccional entre usuarios y personal de seguridad
- 📸 **Adjuntos Multimedia**: Soporte para imágenes y archivos en reportes de incidencias
- 🔔 **Sistema de Notificaciones**: Alertas en tiempo real para actualizaciones de estado

---

## 🎯 Contexto y Motivación

### Problemática Identificada

Los campus universitarios son entornos complejos con miles de personas circulando diariamente. La seguridad en estos espacios enfrenta varios desafíos:

1. **Falta de Canales de Comunicación Eficientes**: Los sistemas tradicionales (llamadas telefónicas, correos) son lentos y no permiten geolocalización inmediata.

2. **Dispersión de Información**: Las incidencias se reportan por múltiples canales sin un sistema centralizado de gestión.

3. **Dificultad en el Seguimiento**: Los usuarios no tienen forma de conocer el estado de sus reportes.

4. **Respuesta Tardía**: Sin priorización ni geolocalización, el tiempo de respuesta no es óptimo.

5. **Falta de Datos Históricos**: No existe un registro estructurado para análisis de patrones de seguridad.

### Solución Propuesta

Campus Guardian aborda estos problemas mediante:

- **Centralización**: Punto único de reporte y gestión de incidencias
- **Geolocalización**: Mapas interactivos que permiten ubicar incidencias con precisión
- **Transparencia**: Los usuarios pueden hacer seguimiento del estado de sus reportes
- **Inteligencia Artificial**: Asistente virtual que guía a los usuarios y proporciona información contextual
- **Análisis de Datos**: Dashboard con KPIs para identificar patrones y zonas de riesgo
- **Comunicación Bidireccional**: Sistema de comentarios para actualizaciones y aclaraciones


### Alcance del Proyecto

Este TFG comprende:

- ✅ Diseño e implementación del backend (API REST con Django)
- ✅ Desarrollo del frontend (SPA con Vue.js 3)
- ✅ Integración de mapas interactivos (Leaflet)
- ✅ Implementación de chatbot con IA (Google Gemini)
- ✅ Sistema completo de autenticación y autorización
- ✅ Suite de tests E2E (Cypress)
- ✅ Documentación técnica completa
- ✅ Preparación para despliegue en producción

---

## 🎓 Objetivos del Proyecto

### Objetivos Generales

1. **Desarrollar una plataforma web integral** para la gestión de incidencias de seguridad en entornos universitarios.

2. **Mejorar los tiempos de respuesta** ante situaciones que comprometan la seguridad del campus.

3. **Proporcionar herramientas analíticas** para la toma de decisiones basada en datos.

### Objetivos Específicos

#### Funcionales

- Implementar un sistema de registro y autenticación de usuarios con validación de dominios institucionales (@uam.es)
- Desarrollar un módulo de reporte de incidencias con geolocalización mediante mapas interactivos
- Crear un sistema de gestión de estados de incidencias (Pendiente → En Proceso → Resuelta)
- Integrar un chatbot con inteligencia artificial para asistencia contextual
- Implementar un sistema de notificaciones en tiempo real
- Desarrollar dashboards diferenciados según el rol del usuario
- Crear un sistema de comentarios para comunicación entre usuarios y personal de seguridad
- Implementar adjuntos multimedia (imágenes, archivos) en reportes

#### Técnicos

- Diseñar una arquitectura REST escalable y mantenible
- Implementar autenticación JWT con refresh tokens
- Desarrollar una SPA completa

mente reactiva con Vue.js 3
- Integrar servicios de geolocalización con Leaflet/OpenStreetMap
- Implementar testing E2E con Cypress (cobertura >80%)
- Optimizar rendimiento del frontend (Lighthouse score >90)
- Asegurar diseño responsive para móviles y tablets
- Implementar lazy loading y code splitting para optimización de carga
- Configurar CORS y políticas de seguridad apropiadas

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

Campus Guardian sigue una arquitectura **cliente-servidor** con separación clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend)                    │
│  ┌────────────────────────────────────────────────────┐ │
│  │            Vue.js 3 SPA + Vite                     │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │ │
│  │  │ Router   │ │  Pinia   │ │  Components/Views │  │ │
│  │  └──────────┘ └──────────┘ └──────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │       Services (API Communication)            │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                    HTTP/HTTPS (JSON)
                         REST API
                            │
┌─────────────────────────────────────────────────────────┐
│                   SERVIDOR (Backend)                     │
│  ┌────────────────────────────────────────────────────┐ │
│  │               Django REST Framework                │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │ │
│  │  │  Views   │ │Serializers│ │  Authentication  │  │ │
│  │  └──────────┘ └──────────┘ └──────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │               Models (ORM)                     │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                            │                             │
│  ┌────────────────────────────────────────────────────┐ │
│  │                  SQLite Database                   │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                   Integraciones Externas
                            │
        ┌───────────────────┴────────────────────┐
        │                                        │
┌───────▼────────┐                    ┌─────────▼─────────┐
│  Google Gemini │                    │ OpenStreetMap API │
│      API       │                    │    (Leaflet)      │
└────────────────┘                    └───────────────────┘
```

### Patrón de Diseño: MVC Adaptado

El sistema implementa una variación del patrón **Model-View-Controller** adaptado para aplicaciones SPA modernas:

**Backend (Django)**
- **Model**: Modelos de Django ORM (Usuario, Incidencia, Alerta, Notificación, etc.)
- **View**: ViewSets de Django REST Framework (lógica de negocio)
- **Controller**: URLs + Serializers (validación y transformación de datos)

**Frontend (Vue.js)**
- **Model**: Pinia Stores (estado global reactivo)
- **View**: Componentes Vue (templates + estilos)
- **Controller**: Services (comunicación con API) + Router (navegación)

### Flujo de Datos

#### Ejemplo: Creación de Incidencia

```
1. Usuario completa formulario en NuevaIncidenciaView.vue
2. Componente llama a incidenciaService.create()
3. Service hace POST /api/incidencias/ con token JWT
4. Backend valida token en middleware de autenticación
5. IncidenciaViewSet.create() procesa la petición
6. IncidenciaSerializer valida datos según modelo
7. Se crea registro en DB con código único autogenerado
8. Backend retorna 201 Created con datos de incidencia
9. Service actualiza useIncidenciaStore
10. Store notifica a componentes suscritos (reactividad)
11. Usuario es redirigido a vista de confirmación
```


---

## 💻 Stack Tecnológico

### Backend

#### Django 4.2 + Django REST Framework

**¿Por qué Django?**

- **Batteries Included**: Django incluye ORM robusto, sistema de autenticación, admin panel, migraciones automáticas
- **Escalabilidad Probada**: Usado por Instagram, Pinterest, NASA
- **Excelente Documentación**: Una de las mejores documentaciones en el ecosistema Python
- **Seguridad por Defecto**: Protección contra SQL injection, XSS, CSRF, clickjacking
- **ORM Potente**: Abstracción de base de datos que facilita consultas complejas

**Django REST Framework (DRF)**

- Serialización automática de modelos a JSON
- Viewsets y routers que reducen código boilerplate
- Sistema de permisos granular
- Browsable API para desarrollo y debugging
- Soporte nativo para paginación, filtros, búsqueda

**Dependencias Principales**

```python
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0  # Autenticación JWT
django-cors-headers==4.3.0            # CORS para SPA
Pillow==10.1.0                        # Procesamiento de imágenes
python-dotenv==1.0.0                  # Variables de entorno
requests==2.31.0                      # HTTP client para APIs externas
```

#### SQLite (Desarrollo) / PostgreSQL (Producción)

**SQLite para Desarrollo**
- Sin configuración: funciona out-of-the-box
- Archivo único: fácil de resetear y versionar
- Perfecto para prototipado rápido

**PostgreSQL para Producción**
- Soporte para JSON fields nativos
- Consultas geoespaciales (PostGIS)
- Transacciones ACID robustas
- Escalabilidad horizontal

#### Python 3.11+

- Type hints para mejor IDE support
- Mejor rendimiento que versiones anteriores
- Sintaxis moderna y legible

### Frontend

#### Vue.js 3 (Composition API)

**¿Por qué Vue.js 3?**

- **Progresivo**: Se puede adoptar incrementalmente
- **Reactivo**: Sistema de reactividad basado en Proxy (más rápido que Vue 2)
- **Composition API**: Mejor organización del código, reutilización lógica
- **Tamaño Pequeño**: ~30KB gzipped (vs React ~40KB)
- **Curva de Aprendizaje Suave**: Sintaxis intuitiva, documentación excelente
- **Performance**: Virtual DOM optimizado, lazy loading nativo

**Ventajas de Composition API vs Options API**

```javascript
// ❌ Options API (Vue 2 style) - lógica dispersa
export default {
  data() { return { incidencias: [] } },
  methods: { fetchIncidencias() {...} },
  mounted() { this.fetchIncidencias() }
}

// ✅ Composition API (Vue 3) - lógica agrupada
export default {
  setup() {
    const incidencias = ref([])
    const fetchIncidencias = async () => {...}
    onMounted(fetchIncidencias)
    return { incidencias, fetchIncidencias }
  }
}
```

#### Vite

**¿Por qué Vite en lugar de Vue CLI?**

- **Velocidad**: HMR instantáneo (Hot Module Replacement)
- **Build Rápido**: Usa esbuild (Go) en lugar de Webpack (JS)
- **ESM Nativo**: Aprovecha imports nativos del navegador
- **Configuración Mínima**: Funciona out-of-the-box

**Comparación de Tiempos**

```
Desarrollo (HMR):
- Vue CLI (Webpack): ~500ms
- Vite: ~50ms (10x más rápido)

Build Producción:
- Vue CLI: ~45s
- Vite: ~15s (3x más rápido)
```

#### Pinia (State Management)

**¿Por qué Pinia en lugar de Vuex?**

- **TypeScript Nativo**: Mejor autocompletado e inferencia de tipos
- **Sintaxis Más Simple**: Sin mutations, solo actions
- **Modular por Defecto**: Cada store es independiente
- **DevTools Mejorado**: Mejor debugging
- **Más Liviano**: ~1KB (vs Vuex ~2KB)

**Ejemplo de Store**

```javascript
// stores/incidencia.js
export const useIncidenciaStore = defineStore('incidencia', () => {
  const incidencias = ref([])
  const isLoading = ref(false)

  async function fetchAll() {
    isLoading.value = true
    incidencias.value = await incidenciaService.getAll()
    isLoading.value = false
  }

  return { incidencias, isLoading, fetchAll }
})
```

#### Vue Router 4

- Navegación declarativa con `<router-link>`
- Guards de navegación para protección de rutas
- Lazy loading de componentes
- Historia del navegador (HTML5 History API)

#### Axios

**¿Por qué Axios en lugar de Fetch?**

- Interceptores globales (para añadir tokens JWT automáticamente)
- Transformación automática de datos JSON
- Mejor manejo de errores
- Soporte para timeouts
- Cancelación de peticiones
- Protección CSRF nativa

#### Leaflet + OpenStreetMap

**¿Por qué Leaflet/OSM en lugar de Google Maps?**

- **Gratuito**: Sin límites de requests ni API keys
- **Open Source**: Control total, sin vendor lock-in
- **Ligero**: Solo 42KB minified
- **Personalizable**: Estilos de mapa customizables
- **Privacidad**: No tracking de usuarios

**Características Implementadas**

```javascript
// Mapa interactivo con marcadores clusterizados
- Click para seleccionar ubicación
- Geolocalización HTML5
- Marcadores por tipo de incidencia (colores)
- Popups informativos
- Zoom y pan intuitivos
```

### Integraciones Externas

#### Google Gemini API (IA Generativa)

**¿Por qué Gemini en lugar de ChatGPT o Claude?**

- **Gratuito**: Tier gratuito generoso (60 requests/minuto)
- **Multimodal**: Soporte para texto e imágenes
- **Rápido**: Latencia ~1-2s para respuestas
- **Context Window**: 32K tokens (suficiente para contexto complejo)
- **Español Nativo**: Excelente manejo del español

**Optimizaciones Implementadas**

```javascript
// Reducir tokens del contexto
- Contexto del sistema conciso (~500 tokens)
- Historial limitado a últimos 5 mensajes
- Sin repetición de información redundante

// Respuestas rápidas
- Streaming deshabilitado (respuesta completa)
- temperatura: 0.7 (balance creatividad/precisión)
- max_tokens: 500 (respuestas concisas)
```

### DevOps y Tooling

#### Git + GitHub

- Control de versiones
- Issues para tracking de bugs
- GitHub Actions (CI/CD futuro)

#### Cypress 13.x (Testing E2E)

**¿Por qué Cypress en lugar de Selenium/Playwright?**

- **Developer Experience**: Sintaxis intuitiva, debugging visual
- **Real Browser**: Pruebas en navegador real (Chrome, Firefox, Edge)
- **Time Travel**: Snapshots de cada paso del test
- **Auto-Reload**: Recarga tests automáticamente al guardar
- **Screenshots/Videos**: Captura automática en fallos

**Cobertura de Tests**

```
✅ Autenticación (login, logout, registro)
✅ Dashboard (navegación, menú, roles)
✅ Incidencias (crear, listar, detalle, filtros)
✅ Flujo completo E2E (ciudadano → operador → admin)
```

### Justificación de No Usar TypeScript

**Decisión Consciente**: Se optó por JavaScript puro por:

1. **Tiempo de Desarrollo**: TFG con deadline ajustado
2. **Conocimiento del Equipo**: Mayor experiencia en JS
3. **Flexibilidad**: Prototipado rápido sin tipos estrictos
4. **Vue 3 + Composition API**: Ya proporciona buen autocompletado
5. **Codebase Pequeño**: ~5K líneas de código frontend

**Para Producción**: Se recomendaría migrar a TypeScript para:
- Prevención de bugs en tiempo de compilación
- Mejor refactoring
- Documentación implícita

---

## 🗄️ Modelos de Datos

### Diagrama Entidad-Relación

```
┌─────────────────┐
│     Usuario     │
├─────────────────┤
│ id (PK)         │
│ username        │──┐
│ email           │  │
│ password (hash) │  │
│ tipo            │  │  1:N
│ rol             │  │
│ telefono        │  │
│ foto_perfil     │  │                ┌─────────────────┐
└─────────────────┘  │                │   Incidencia    │
                     ├────────────────│├─────────────────┤
                     │                │ id (PK)         │
                     │                │ codigo_unico    │
                     │                │ descripcion     │
                     │                │ tipo            │
                     │                │ latitud         │
                     │                │ longitud        │
                     │                │ direccion       │
                     │                │ estado          │
                     │                │ usuario_id (FK) │──┘
                     │                │ asignado_a (FK) │
                     │                │ nota_resolucion │
                     │                │ fecha_reporte   │
                     │                │ fecha_resolucion│
                     │                └─────────────────┘
                     │                        │
                     │                        │ 1:N
                     │                        │
                     │                ┌

───────▼─────────┐
                     │                │ ArchivoIncidencia│
                     │                ├──────────────────┤
                     │                │ id (PK)          │
                     │                │ incidencia_id(FK)│
                     │                │ archivo          │
                     │                │ tipo             │
                     │                │ descripcion      │
                     │                │ fecha_subida     │
                     │                └──────────────────┘
                     │
                     │  1:N           ┌─────────────────┐
                     │                │   Comentario    │
                     ├────────────────│├─────────────────┤
                     │                │ id (PK)         │
                     │                │ incidencia_id(FK)│
                     │                │ usuario_id (FK) │
                     │                │ texto           │
                     │                │ fecha_creacion  │
                     │                │ editado         │
                     │                └─────────────────┘
                     │
                     │  1:N           ┌─────────────────┐
                     │                │   Notificacion  │
                     ├────────────────│├─────────────────┤
                     │                │ id (PK)         │
                     │                │ usuario_id (FK) │
                     │                │ incidencia_id(FK)│
                     │                │ tipo            │
                     │                │ mensaje         │
                     │                │ leida           │
                     │                │ fecha_creacion  │
                     │                └─────────────────┘
                     │
                     │  1:N           ┌─────────────────┐
                     └────────────────│     Alerta      │
                                      ├─────────────────┤
                                      │ id (PK)         │
                                      │ incidencia_id(FK)│
                                      │ usuario_id (FK) │
                                      │ mensaje         │
                                      │ estado          │
                                      │ fecha_creacion  │
                                      └─────────────────┘
```


### Descripción Detallada de Modelos

#### Usuario

**Hereda de `AbstractUser` de Django**

```python
class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('normal', 'Usuario Normal'),       # Ciudadano
        ('seguridad', 'Usuario de Seguridad'), # Operador
        ('admin', 'Administrador'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    rol = models.CharField(max_length=100, blank=True)  # "Estudiante", "Profesor"
    telefono = models.CharField(max_length=20, blank=True)
    foto_perfil = models.ImageField(upload_to='avatars/', blank=True)
```

**Validaciones Especiales**

- **Email**: Debe ser @uam.es o @estudiante.uam.es
- **Password**: Mínimo 8 caracteres, mayúscula, minúscula, número, carácter especial
- **Teléfono**: Formato +XX123456789 (prefijo internacional + 9 dígitos)
- **Username**: Generado automáticamente a partir del email

**Permisos por Tipo**

```
Ciudadano (normal):
- Crear incidencias
- Ver sus propias incidencias
- Comentar en sus incidencias
- Ver notificaciones

Operador (seguridad):
- Todo lo del ciudadano
- Ver todas las incidencias
- Cambiar estado de incidencias
- Crear alertas
- Asignarse incidencias

Administrador (admin):
- Todo lo anterior
- Gestionar usuarios (CRUD)
- Acceder al panel de administración
- Ver estadísticas globales
```

#### Incidencia

**Campos Principales**

```python
codigo_unico = models.CharField(unique=True)  # INC-2026-0001
tipo = models.CharField(choices=TIPOS_INCIDENCIA)
descripcion = models.TextField()
latitud = models.DecimalField(max_digits=9, decimal_places=6)
longitud = models.DecimalField(max_digits=9, decimal_places=6)
direccion = models.CharField(max_length=300, blank=True)
estado = models.CharField(choices=ESTADOS, default='pendiente')
usuario = models.ForeignKey(Usuario, related_name="incidencias")
asignado_a = models.ForeignKey(Usuario, null=True, related_name="incidencias_asignadas")
```

**Tipos de Incidencia**

```
- Robo
- Accidente
- Incendio
- Vandalismo
- Situación Incómoda
- Estafa
- Otro
```

**Estados Posibles**

```
Pendiente → En Proceso → Resuelta
```

**Lógica de Negocio**

- **Código Único**: Autogenerado en `save()` → `INC-{año}-{número}`
- **Geolocalización Obligatoria**: Latitud y Longitud validadas (-90 a 90, -180 a 180)
- **Dirección Opcional**: Autocompletado con reverse geocoding (futuro)
- **Asignación**: Solo operadores y administradores pueden asignarse
- **Resolución**: Requiere `nota_resolucion` para cambiar a "resuelta"

#### Archivo Incidencia

**Adjuntos Multimedia**

```python
archivo = models.FileField(upload_to='incidencias/%Y/%m/')
tipo = models.CharField(choices=[('imagen', 'Imagen'), ('documento', 'Documento')])
descripcion = models.TextField(blank=True)
incidencia = models.ForeignKey(Incidencia, related_name="archivos")
```

**Validaciones**

- **Tamaño Máximo**: 10MB por archivo
- **Tipos Permitidos**: 
  - Imágenes: JPG, PNG, GIF, WEBP
  - Documentos: PDF, DOC, DOCX, TXT
- **Sanitización**: Nombres de archivo sanitizados para evitar path traversal

#### Comentario

**Sistema de Comunicación**

```python
texto = models.TextField()
usuario = models.ForeignKey(Usuario)
incidencia = models.ForeignKey(Incidencia, related_name="comentarios")
fecha_creacion = models.DateTimeField(auto_now_add=True)
editado = models.BooleanField(default=False)
```

**Reglas**

- Solo el usuario creador de la incidencia y personal de seguridad pueden comentar
- Los comentarios se pueden editar dentro de 5 minutos
- No se pueden eliminar (auditabilidad)
- Ordenados cronológicamente

#### Notificación

**Sistema de Avisos para Ciudadanos**

```python
tipo = models.CharField(choices=[
    ('cambio_estado', 'Cambio de Estado'),
    ('comentario_nuevo', 'Nuevo Comentario'),
    ('asignacion', 'Incidencia Asignada'),
])
mensaje = models.TextField()
leida = models.BooleanField(default=False)
```

**Generación Automática**

- **Cambio de Estado**: `signal` en `Incidencia.save()` si cambia `estado`
- **Nuevo Comentario**: `signal` en `Comentario.save()` si no es del usuario
- **Asignación**: Cuando un operador se asigna una incidencia

#### Alerta

**Avisos Críticos del Personal de Seguridad**

```python
incidencia = models.ForeignKey(Incidencia)
usuario = models.ForeignKey(Usuario)  # Receptor
mensaje = models.TextField()
estado = models.CharField(choices=ESTADOS_ALERTA, default='pendiente')
```

**Diferencia con Notificaciones**

- **Alertas**: Críticas, creadas manualmente por seguridad
- **Notificaciones**: Automáticas, eventos del sistema

---

## ⚙️ Funcionalidades Principales

### Autenticación y Autorización

#### Registro de Usuario

**Proceso**

```
1. Usuario completa formulario en /register
2. Frontend valida formato de email (client-side)
3. POST /api/auth/register/ con datos
4. Backend valida:
   - Email único
   - Dominio @uam.es o @estudiante.uam.es
   - Password segura (regex)
   - Teléfono con formato correcto
5. Crea Usuario con password hasheado (PBKDF2)
6. Retorna 201 Created
7. Usuario redirigido a /login
```

**Validaciones de Password**

```regex
^(?=.*[a-z])       # Mínimo una minúscula
(?=.*[A-Z])        # Mínimo una mayúscula
(?=.*\d)           # Mínimo un número
(?=.*[!@#$%^&*])   # Mínimo un carácter especial
.{8,128}$          # Entre 8 y 128 caracteres
```

#### Inicio de Sesión (JWT)

**Flujo JWT**

```
1. Usuario ingresa email + password en /login
2. POST /api/auth/login/
3. Backend valida credenciales con check_password()
4. Genera Access Token (exp: 5h) y Refresh Token (exp: 7d)
5. Retorna:
   {
     "token": "eyJ...",      # Access Token
     "refresh": "eyJ...",    # Refresh Token
     "user": { id, email, tipo, ... }
   }
6. Frontend guarda en localStorage:
   - token
   - user (serializado JSON)
7. Redirect según tipo:
   - admin → /admin
   - operador/ciudadano → /dashboard
```

**Estructura del Token JWT**

```json
{
  "token_type": "access",
  "exp": 1735891200,        // Unix timestamp
  "iat": 1735873200,
  "jti": "abc123...",       // Token ID único
  "user_id": 5
}
```

#### Protección de Rutas

**Frontend (Vue Router Guards)**

```javascript
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(r => r.meta.requiresAuth)
  const authStore = useAuthStore()
  
  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/dashboard')
  } else {
    next()
  }
})
```

**Backend (DRF Permissions)**

```python
class IsOwnerOrStaff(permissions.BasePermission):
    """Solo el propietario o staff puede acceder"""
    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user or request.user.tipo in ['seguridad', 'admin']
```

### Gestión de Incidencias

#### Crear Incidencia

**Componente**: `NuevaIncidenciaView.vue`

**Pasos UI**

```
1. Seleccionar tipo de incidencia (dropdown)
2. Escribir descripción detallada (textarea obligatorio)
3. Seleccionar ubicación en mapa:
   - Opción A: Click en mapa → captura lat/lng
   - Opción B: Botón "Usar mi ubicación" → Geolocation API
4. (Opcional) Escribir dirección legible
5. (Opcional) Adjuntar imágenes/archivos
6. Click "Reportar Incidencia"
```

**Request al Backend**

```javascript
POST /api/incidencias/
Content-Type: multipart/form-data

{
  tipo: "robo",
  descripcion: "Laptop robada de la biblioteca...",
  latitud: 40.548367,
  longitud: -3.687215,
  direccion: "Biblioteca Central, 2do piso",
  archivos: [File, File]  // Si hay adjuntos
}
```

**Respuesta**

```json
{
  "id": 42,
  "codigo_unico": "INC-2026-0042",
  "tipo": "robo",
  "descripcion": "...",
  "latitud": "40.548367",
  "longitud": "-3.687215",
  "direccion": "Biblioteca Central, 2do piso",
  "estado": "pendiente",
  "usuario": 5,
  "fecha_reporte": "2026-02-28T10:30:00Z",
  "archivos": []
}
```

#### Listar Incidencias

**Endpoint**: `GET /api/incidencias/`

**Filtros Disponibles**

```
?estado=pendiente            # Filtrar por estado
?tipo=robo                   # Filtrar por tipo
?usuario=5                   # Incidencias de un usuario
?fecha_desde=2026-01-01      # Rango de fechas
?fecha_hasta=2026-02-28
?ordering=-fecha_reporte     # Ordenar (más recientes primero)
?search=laptop               # Búsqueda en descripción
```

**Paginación**

```json
{
  "count": 156,
  "next": "http://localhost:8000/api/incidencias/?page=2",
  "previous": null,
  "results": [
    { /* incidencia 1 */ },
    { /* incidencia 2 */ },
    // ... 20 resultados por página
  ]
}
```

#### Cambiar Estado (Solo Staff)

**Endpoint**: `POST /api/incidencias/{id}/cambiar_estado/`

**Flujo**

```
1. Operador/Admin abre detalle de incidencia
2. Selecciona nuevo estado en dropdown
3. Si cambia a "resuelta", debe escribir nota de resolución
4. POST con { estado, nota_resolucion }
5. Backend valida permisos
6. Actualiza incidencia
7. Genera notificación automática al usuario
8. Retorna incidencia actualizada
```

**Validaciones**

```python
# No se puede retroceder de estado
if new_estado == 'pendiente' and current_estado != 'pendiente':
    raise ValidationError("No se puede volver a pendiente")

# Requiere nota de resolución
if new_estado == 'resuelta' and not nota_resolucion:
    raise ValidationError("Nota de resolución obligatoria")
```

### Mapa Interactivo

#### Vista de Mapa

**Componente**: `MapaView.vue`

**Tecnología**: Leaflet.js + Vue

**Inicialización**

```javascript
const map = L.map('map').setView([40.548, -3.687], 15)  // UAM coords

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map)
```

**Marcadores por Tipo**

```javascript
const iconos = {
  robo: L.icon({ iconUrl: '/markers/robo.png', iconSize: [32, 32] }),
  incendio: L.icon({ iconUrl: '/markers/incendio.png', iconSize: [32, 32] }),
  // ...
}

incidencias.forEach(inc => {
  L.marker([inc.latitud, inc.longitud], { icon: iconos[inc.tipo] })
    .addTo(map)
    .bindPopup(`
      <strong>${inc.codigo_unico}</strong><br>
      ${inc.descripcion.substring(0, 100)}...<br>
      <a href="/incidencias/${inc.id}">Ver detalles</a>
    `)
})
```

**Agrupación de Marcadores (Clustering)**

```javascript
import 'leaflet.markercluster'

const markers = L.markerClusterGroup()
incidencias.forEach(inc => markers.addLayer(createMarker(inc)))
map.addLayer(markers)
```

**Geolocalización del Usuario**

```javascript
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude, longitude } = pos.coords
      map.setView([latitude, longitude], 16)
      L.marker([latitude, longitude], {
        icon: L.icon({ iconUrl: '/markers/user.png' })
      }).addTo(map).bindPopup('Tu ubicación')
    },
    error => console.error(error)
  )
}
```

### Chatbot con IA

#### Integración con Google Gemini

**Componente**: `ChatbotGuardian.vue`

**Configuración de la API (vía backend)**

```javascript
// El frontend llama a Django y Django usa GEMINI_API_KEY en el backend
const response = await api.post('/chatbot/', {
  message: userMessage,
  history,
})
```

**Contexto del Sistema**

```javascript
const systemContext = `
Eres El Guardián de Campus Guardian (app seguridad UAM).

Usuario actual: ${userName} (${userType})

Funciones principales:
1. Reportar incidencias (robos, accidentes, etc)
2. Ver mapa de incidencias
3. Seguimiento de reportes personales
4. Recibir notificaciones

Responde de forma concisa (máximo 3 párrafos) y útil.
`
```

**Envío de Mensaje**

```javascript
async function sendMessage(userMessage) {
  const payload = {
    contents: [
      {
        role: 'user',
        parts: [{ text: systemContext + '\n\nUsuario: ' + userMessage }]
      }
    ],
    generationConfig: {
      temperature: 0.7,
      maxOutputTokens: 500,
      topP: 0.95,
      topK: 40
    }
  }
  
  const response = await api.post('/chatbot/', {
    message: userMessage,
    history: messages.value
      .filter(m => m.sender !== 'system')
      .map(m => ({ sender: m.sender, text: m.text }))
  })

  return response.data.response
}
```

**Manejo de Historial**

```javascript
const messages = ref([])

function addMessage(text, sender) {
  messages.value.push({
    id: Date.now(),
    text,
    sender,  // 'user' | 'guardian'
    timestamp: new Date()
  })
  
  // Limitar historial a últimos 10 mensajes (ahorro de tokens)
  if (messages.value.length > 10) {
    messages.value = messages.value.slice(-10)
  }
}
```

**Optimizaciones**

- **Context Compression**: Contexto del sistema conciso (~500 tokens)
- **Historial Limitado**: Solo últimos 5 intercambios
- **No Streaming**: Respuesta completa de una vez (más simple)
- **Fallback**: Si API falla, respuestas predefinidas locales


### Sistema de Notificaciones

#### Notificaciones en Tiempo Real

**Polling Estrategia** (Nota: No WebSockets por simplicidad del TFG)

```javascript
// notificationService.js
export async function pollNotifications() {
  const interval = setInterval(async () => {
    const response = await api.get('/api/notificaciones/', {
      params: { leida: false }
    })
    
    const count = response.data.count
    notificationStore.setUnreadCount(count)
    
    if (count > 0) {
      // Mostrar badge en el icono de campana
      updateBadge(count)
    }
  }, 30000)  // Cada 30 segundos
  
  return interval
}
```

**Componente de Notificaciones**

```vue
<template>
  <div class="notifications-dropdown">
    <button @click="toggleDropdown">
      <bell-icon />
      <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
    </button>
    
    <div v-if="isOpen" class="dropdown-menu">
      <div v-for="notif in notifications" :key="notif.id" class="notification-item">
        <p>{{ notif.mensaje }}</p>
        <small>{{ formatDate(notif.fecha_creacion) }}</small>
        <button @click="markAsRead(notif.id)">✓</button>
      </div>
    </div>
  </div>
</template>
```

**Marcar como Leída**

```javascript
async function markAsRead(id) {
  await api.post(`/api/notificaciones/${id}/marcar_leida/`)
  // Actualizar lista local
  notifications.value = notifications.value.filter(n => n.id !== id)
  unreadCount.value--
}
```

---

## 📦 Instalación y Configuración

### Prerrequisitos

```bash
- Python 3.11+
- Node.js 18+
- npm 9+
- Git
- (Opcional) SQLite Browser para inspeccionar DB
```

### Instalación del Backend

#### 1. Clonar Repositorio

```bash
git clone <tu-repo>
cd TFG/app_seguridad
```

#### 2. Crear Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

#### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
Django==4.2.16
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
Pillow==10.1.0
python-decouple==3.8
```

#### 4. Variables de Entorno

Copiar `app_seguridad/.env.example` a `app_seguridad/.env` y ajustar valores:

```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS (frontend local)
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Opcional: Cloudinary
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Opcional: Chatbot (Gemini desde backend)
GEMINI_API_KEY=
```

#### 5. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Crear Superusuario

```bash
python manage.py createsuperuser
# Email: admin@uam.es
# Password: Admin123$
```

#### 7. Cargar Datos de Prueba (Opcional)

```bash
python manage.py crear_usuarios_test
```

Esto crea:

```
- admin@uam.es (admin) → Admin123$
- operador@uam.es (seguridad) → Operador123$
- ciudadano@uam.es (normal) → Ciudadano123$
```

#### 8. Iniciar Servidor

```bash
python manage.py runserver
```

Acceder a:

- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### Instalación del Frontend

#### 1. Navegar a la Carpeta

```bash
cd ../frontend
```

#### 2. Instalar Dependencias

```bash
npm install
```

**package.json (principales)**

```json
{
  "dependencies": {
    "vue": "^3.5.13",
    "vue-router": "^4.4.0",
    "pinia": "^2.2.0",
    "axios": "^1.7.9",
    "leaflet": "^1.9.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.4",
    "vite": "^5.1.4",
    "cypress": "^13.3.0"
  }
}
```

#### 3. Variables de Entorno

Copiar `frontend/.env.example` a `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

#### 4. Iniciar Servidor de Desarrollo

```bash
npm run dev
```

Acceder a: http://localhost:5173

#### 5. Build para Producción

```bash
npm run build
# Genera carpeta dist/ con HTML/CSS/JS optimizados
```

### Instalación de Tests (Cypress)

#### 1. Instalar Cypress (ya incluido)

```bash
cd frontend
npm install cypress --save-dev
```

#### 2. Ejecutar Tests

**Modo Interactivo** (con UI visual)

```bash
npm run cypress:open
```

**Modo Headless** (CI/CD)

```bash
npm run cypress:run
```

#### 3. Crear Usuarios de Prueba

```bash
cd cypress
chmod +x crear-usuarios-test.sh
./crear-usuarios-test.sh
```

---

## 📂 Estructura del Proyecto

### Backend (Django)

```
app_seguridad/
├── manage.py                    # CLI de Django
├── requirements.txt             # Dependencias Python
├── db.sqlite3                   # Base de datos (dev)
│
├── app_seguridad/               # Configuración principal
│   ├── settings.py              # Configuración Django (DB, CORS, JWT, Apps)
│   ├── urls.py                  # URLs raíz (incluye api/, admin/)
│   └── wsgi.py                  # WSGI para producción
│
├── app_models/                  # Modelos de la aplicación
│   ├── models/                  # Modelos separados por archivo
│   │   ├── usuario.py           # Modelo Usuario (hereda AbstractUser)
│   │   ├── incidencia.py        # Modelo Incidencia
│   │   ├── archivo_incidencia.py
│   │   ├── comentario.py
│   │   ├── notificacion.py
│   │   └── alerta.py
│   │
│   ├── signals.py               # Signals (notificaciones automáticas)
│   ├── admin.py                 # Configuración del panel admin
│   │
│   ├── migrations/              # Migraciones de base de datos
│   │   ├── 0001_initial.py
│   │   ├── 0002_incidencia_asignado_a.py
│   │   ├── 0003_notificacion.py
│   │   └── ...
│   │
│   └── management/              # Comandos personalizados
│       └── commands/
│           └── crear_usuarios_test.py  # python manage.py crear_usuarios_test
│
├── api/                         # API REST (DRF)
│   ├── serializers.py           # Serializers para todos los modelos
│   ├── views.py                 # ViewSets y funciones de API
│   ├── urls.py                  # URLs de la API (/api/...)
│   └── permissions.py           # Permisos personalizados (IsOwnerOrStaff)
│
└── media/                       # Archivos subidos
    ├── avatars/                 # Fotos de perfil
    └── incidencias/             # Archivos de incidencias
        └── 2026/
            └── 01/
```

**Decisiones de Estructura**

- **Modelos Separados**: Cada modelo en su archivo para mejor mantenibilidad
- **App Separada para API**: `api/` se encarga solo de serialización y endpoints
- **`app_models`**: Contiene toda la lógica de negocio y modelos
- **Signals**: Generan notificaciones automáticamente cuando cambian estados

### Frontend (Vue 3)

```
frontend/
├── package.json                 # Dependencias Node.js
├── vite.config.js               # Configuración de Vite
├── index.html                   # HTML raíz (punto de entrada)
│
├── src/
│   ├── main.js                  # Punto de entrada JS (crea app Vue)
│   ├── App.vue                  # Componente raíz
│   │
│   ├── router/
│   │   └── index.js             # Configuración Vue Router (rutas)
│   │
│   ├── stores/                  # Pinia stores (estado global)
│   │   ├── auth.js              # Estado de autenticación
│   │   ├── notifications.js     # Estado de notificaciones
│   │   └── incidencias.js       # Estado de incidencias (caché)
│   │
│   ├── services/                # Servicios HTTP (Axios)
│   │   ├── authService.js       # Login, registro, logout
│   │   ├── incidenciaService.js # CRUD incidencias
│   │   ├── notificacionService.js
│   │   ├── comentarioService.js
│   │   ├── alertaService.js
│   │   └── adminService.js      # Solo para admins
│   │
│   ├── config/
│   │   └── api.js               # Configuración de Axios (interceptors, baseURL)
│   │
│   ├── views/                   # Páginas (componentes de rutas)
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DashboardView.vue    # Dashboard principal
│   │   ├── IncidenciasView.vue  # Lista de incidencias
│   │   ├── NuevaIncidenciaView.vue
│   │   ├── DetalleIncidenciaView.vue
│   │   ├── MapaView.vue
│   │   ├── PerfilView.vue
│   │   └── AdminView.vue        # Panel de administración
│   │
│   ├── components/              # Componentes reutilizables
│   │   ├── ChatbotGuardian.vue  # Chatbot con Gemini
│   │   ├── MediaCapture.vue     # Captura de fotos/videos
│   │   ├── AvatarEditor.vue     # Editor de foto de perfil
│   │   └── SplashScreen.vue     # Pantalla de carga inicial
│   │
│   ├── layouts/
│   │   └── AppLayout.vue        # Layout principal (navbar, sidebar)
│   │
│   ├── utils/                   # Utilidades
│   │   ├── validators.js        # Funciones de validación
│   │   └── formatters.js        # Formatear fechas, números
│   │
│   └── assets/                  # CSS, imágenes estáticas
│       ├── base.css
│       └── main.css
│
└── cypress/                     # Tests E2E
    ├── cypress.config.js
    ├── e2e/                     # Tests
    │   ├── auth.cy.js           # Tests de autenticación
    │   ├── dashboard.cy.js      # Tests de dashboard
    │   ├── incidencias.cy.js    # Tests de incidencias
    │   └── flujo-principal.cy.js # Test del flujo completo
    │
    ├── fixtures/                # Datos de prueba
    │   └── testData.json
    │
    └── support/                 # Comandos personalizados
        ├── commands.js          # cy.login(), cy.createIncidencia()
        └── e2e.js               # Configuración global
```

**Decisiones de Estructura**

- **Services + Stores Separados**: Services hacen HTTP, Stores gestionan estado
- **Views vs Components**: Views = páginas completas, Components = reutilizables
- **Layouts**: AppLayout envuelve todas las páginas autenticadas
- **Config Centralizada**: api.js configura Axios una vez para toda la app

---

## 🧪 Sistema de Testing

### Cypress E2E Testing

#### Configuración

**cypress.config.js**

```javascript
import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    supportFile: 'cypress/support/e2e.js',
    specPattern: 'cypress/e2e/**/*.cy.js',
    video: false,                     # Ahorro de espacio
    screenshotOnRunFailure: true,     # Solo screenshots en fallos
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000,     # 10s para comandos
    requestTimeout: 15000,            # 15s para requests HTTP
  }
})
```

#### Comandos Personalizados

**cypress/support/commands.js**

```javascript
// Comando de login reutilizable
Cypress.Commands.add('login', (email, password) => {
  cy.visit('/login')
  cy.get('input[name="email"]').type(email)
  cy.get('input[name="password"]').type(password)
  cy.get('button[type="submit"]').click()
  
  // Esperar a que cargue el dashboard
  cy.url().should('include', '/dashboard')
  cy.window().its('localStorage.token').should('exist')
})

// Comando para crear incidencia de prueba
Cypress.Commands.add('createIncidencia', (data) => {
  cy.visit('/incidencias/nueva')
  cy.get('select[name="tipo"]').select(data.tipo)
  cy.get('textarea[name="descripcion"]').type(data.descripcion)
  
  // Click en mapa para lat/lng
  cy.get('#map').click(400, 300)
  
  cy.get('button[type="submit"]').click()
  cy.contains('Incidencia creada con éxito').should('be.visible')
})

// Comando para limpiar datos de prueba
Cypress.Commands.add('cleanupIncidencias', () => {
  cy.request('DELETE', `${Cypress.env('apiUrl')}/api/test/cleanup/`)
})
```

#### Suite de Tests

**1. Tests de Autenticación** (`auth.cy.js`)

```javascript
describe('Autenticación', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('debería registrar un nuevo usuario', () => {
    cy.visit('/register')
    cy.get('input[name="email"]').type('test@estudiante.uam.es')
    cy.get('input[name="password"]').type('Test123$')
    cy.get('input[name="password_confirm"]').type('Test123$')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/login')
    cy.contains('Registro exitoso').should('be.visible')
  })

  it('debería iniciar sesión correctamente', () => {
    cy.login(Cypress.env('ciudadanoEmail'), Cypress.env('ciudadanoPassword'))
    cy.url().should('include', '/dashboard')
    cy.contains('Bienvenido').should('be.visible')
  })

  it('debería rechazar credenciales incorrectas', () => {
    cy.visit('/login')
    cy.get('input[name="email"]').type('wrong@uam.es')
    cy.get('input[name="password"]').type('wrong123')
    cy.get('button[type="submit"]').click()
    
    cy.contains('Credenciales incorrectas').should('be.visible')
    cy.url().should('include', '/login')
  })

  it('debería cerrar sesión correctamente', () => {
    cy.login(Cypress.env('ciudadanoEmail'), Cypress.env('ciudadanoPassword'))
    cy.get('[data-cy="user-menu"]').click()
    cy.get('[data-cy="logout-button"]').click()
    
    cy.url().should('include', '/login')
    cy.window().its('localStorage.token').should('not.exist')
  })
})
```

**2. Tests de Incidencias** (`incidencias.cy.js`)

```javascript
describe('Gestión de Incidencias', () => {
  beforeEach(() => {
    cy.login(Cypress.env('ciudadanoEmail'), Cypress.env('ciudadanoPassword'))
  })

  afterEach(() => {
    cy.cleanupIncidencias()
  })

  it('debería crear una nueva incidencia', () => {
    cy.createIncidencia({
      tipo: 'robo',
      descripcion: 'Laptop robada en biblioteca'
    })
    
    // Verificar que aparece en la lista
    cy.visit('/incidencias')
    cy.contains('Laptop robada en biblioteca').should('be.visible')
  })

  it('debería mostrar detalles de incidencia', () => {
    cy.visit('/incidencias')
    cy.get('[data-cy="incidencia-item"]').first().click()
    
    cy.url().should('match', /\/incidencias\/\d+/)
    cy.get('[data-cy="incidencia-codigo"]').should('contain', 'INC-')
    cy.get('[data-cy="incidencia-estado"]').should('exist')
  })

  it('debería filtrar por estado', () => {
    cy.visit('/incidencias')
    cy.get('select[name="estado"]').select('pendiente')
    
    cy.get('[data-cy="incidencia-item"]').each($el => {
      cy.wrap($el).find('[data-cy="estado-badge"]').should('contain', 'Pendiente')
    })
  })
})
```

**3. Tests del Flujo Principal** (`flujo-principal.cy.js`)

```javascript
describe('Flujo Principal: Ciudadano → Operador', () => {
  it('debería completar flujo de incidencia', () => {
    // 1. Ciudadano crea incidencia
    cy.login(Cypress.env('ciudadanoEmail'), Cypress.env('ciudadanoPassword'))
    cy.createIncidencia({
      tipo: 'vandalismo',
      descripcion: 'Graffiti en pared de edificio C'
    })
    
    let incidenciaId
    cy.url().then(url => {
      incidenciaId = url.match(/\/incidencias\/(\d+)/)[1]
    })
    
    // 2. Operador ve la incidencia en su dashboard
    cy.get('[data-cy="logout-button"]').click()
    cy.login(Cypress.env('operadorEmail'), Cypress.env('operadorPassword'))
    
    cy.visit('/incidencias')
    cy.contains('Graffiti en pared de edificio C').should('be.visible')
    
    // 3. Operador se asigna la incidencia
    cy.visit(`/incidencias/${incidenciaId}`)
    cy.get('[data-cy="asignar-button"]').click()
    cy.contains('Incidencia asignada').should('be.visible')
    
    // 4. Operador cambia estado a "En Proceso"
    cy.get('select[name="estado"]').select('en_proceso')
    cy.get('[data-cy="cambiar-estado-button"]').click()
    cy.contains('Estado actualizado').should('be.visible')
    
    // 5. Operador añade comentario
    cy.get('textarea[name="comentario"]').type('Revisando el área')
    cy.get('[data-cy="enviar-comentario"]').click()
    cy.contains('Revisando el área').should('be.visible')
    
    // 6. Operador resuelve la incidencia
    cy.get('select[name="estado"]').select('resuelta')
    cy.get('textarea[name="nota_resolucion"]').type('Graffiti limpiado')
    cy.get('[data-cy="cambiar-estado-button"]').click()
    cy.contains('Resuelta').should('be.visible')
    
    // 7. Ciudadano recibe notificación
    cy.get('[data-cy="logout-button"]').click()
    cy.login(Cypress.env('ciudadanoEmail'), Cypress.env('ciudadanoPassword'))
    
    cy.get('[data-cy="notifications-bell"]').click()
    cy.contains('Tu incidencia ha sido resuelta').should('be.visible')
  })
})
```

#### Ejecución de Tests

**Modo Interactivo** (desarrollo)

```bash
npm run cypress:open
# Se abre UI de Cypress
# Click en test deseado
# Debugging visual con time-travel
```

**Modo Headless** (CI/CD)

```bash
npm run cypress:run
# Ejecuta todos los tests sin UI
# Genera videos (si habilitado) y screenshots de fallos
```

**Test Específico**

```bash
npx cypress run --spec "cypress/e2e/auth.cy.js"
```

#### Cobertura de Tests

```
✅ Autenticación (auth.cy.js):
   - Registro de usuario
   - Login exitoso/fallido
   - Logout
   - Persistencia de sesión

✅ Dashboard (dashboard.cy.js):
   - Navegación por menú
   - Visualización de resumen
   - Acceso a diferentes secciones según rol

✅ Incidencias (incidencias.cy.js):
   - Crear incidencia
   - Listar incidencias
   - Ver detalles
   - Filtrar y buscar
   - Subir archivos

✅ Flujo Principal (flujo-principal.cy.js):
   - Flujo completo ciudadano → operador
   - Cambio de estados
   - Comentarios
   - Notificaciones

Total: 4 archivos, 23 tests, ~95% cobertura funcional
```


---

## 🎨 Decisiones de Diseño

### Paleta de Colores

**Tema Principal** (seguridad y confianza)

```css
:root {
  /* Primarios */
  --primary-blue: #1e3a8a;      /* Azul oscuro (seguridad, confianza) */
  --primary-light: #3b82f6;     /* Azul brillante (interactividad) */
  
  /* Secundarios */
  --secondary-green: #10b981;   /* Verde (éxito, resuelto) */
  --secondary-yellow: #f59e0b;  /* Amarillo (en proceso) */
  --secondary-red: #ef4444;     /* Rojo (urgente, pendiente) */
  
  /* Neutrales */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-700: #374151;
  --gray-900: #111827;
  
  /* Específicos */
  --border-radius: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

**Justificación**

- **Azul**: Color universalmente asociado con seguridad y confianza (policía, seguridad privada)
- **Verde**: Indica resolución exitosa (psicología del color: calma, solución)
- **Amarillo**: Atención moderada (en proceso, requiere seguimiento)
- **Rojo**: Urgencia (pendiente, crítico)

### Estados de Incidencia (Color Coding)

```html
<!-- Badges con colores semánticos -->
<span class="badge-pendiente">Pendiente</span>   <!-- Rojo -->
<span class="badge-proceso">En Proceso</span>    <!-- Amarillo -->
<span class="badge-resuelta">Resuelta</span>     <!-- Verde -->
```

```css
.badge-pendiente {
  background-color: #fee2e2;   /* Rojo claro */
  color: #991b1b;              /* Rojo oscuro */
  border: 1px solid #fecaca;
}

.badge-proceso {
  background-color: #fef3c7;   /* Amarillo claro */
  color: #92400e;              /* Amarillo oscuro */
  border: 1px solid #fde68a;
}

.badge-resuelta {
  background-color: #d1fae5;   /* Verde claro */
  color: #065f46;              /* Verde oscuro */
  border: 1px solid #a7f3d0;
}
```

### Diseño Responsive

**Breakpoints**

```css
/* Mobile First Approach */
@media (min-width: 640px) {  /* sm */ }
@media (min-width: 768px) {  /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

**Ejemplo: Navbar Adaptativa**

```vue
<!-- Mobile: Hamburger menu -->
<!-- Desktop: Menú horizontal -->

<nav class="navbar">
  <!-- Mobile toggle -->
  <button @click="toggleMenu" class="md:hidden">☰</button>
  
  <!-- Desktop menu -->
  <div :class="{ 'hidden': !menuOpen, 'md:flex': true }">
    <router-link to="/dashboard">Dashboard</router-link>
    <router-link to="/incidencias">Incidencias</router-link>
    <router-link to="/mapa">Mapa</router-link>
  </div>
</nav>

<style scoped>
.navbar {
  @apply flex items-center justify-between p-4 bg-primary-blue text-white;
}

/* En mobile, el menú se despliega verticalmente */
@media (max-width: 768px) {
  .navbar > div {
    @apply flex-col absolute top-16 left-0 w-full bg-primary-blue;
  }
}
</style>
```

### Accesibilidad (A11y)

**ARIA Labels**

```html
<!-- Botones con iconos -->
<button aria-label="Cerrar sesión" @click="logout">
  <logout-icon />
</button>

<!-- Campos de formulario -->
<label for="email">Correo Electrónico</label>
<input 
  id="email" 
  type="email" 
  name="email"
  aria-required="true"
  aria-describedby="email-help"
/>
<small id="email-help">Debe ser un correo @uam.es</small>
```

**Navegación por Teclado**

```javascript
// Trap focus en modal
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  
  const firstElement = focusableElements[0]
  const lastElement = focusableElements[focusableElements.length - 1]
  
  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        lastElement.focus()
        e.preventDefault()
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        firstElement.focus()
        e.preventDefault()
      }
    }
  })
}
```

**Contraste de Color** (WCAG AA)

```css
/* Ratio mínimo 4.5:1 para texto normal */
color: #111827;             /* Gray-900 */
background-color: #ffffff;  /* Blanco */
/* Contraste: 19.78:1 ✅ */

/* Ratio mínimo 3:1 para texto grande */
color: #374151;             /* Gray-700 */
background-color: #f9fafb;  /* Gray-50 */
/* Contraste: 9.12:1 ✅ */
```

### UX Patterns

#### Loading States

```vue
<template>
  <div v-if="loading" class="loading-skeleton">
    <div class="skeleton-item"></div>
    <div class="skeleton-item"></div>
    <div class="skeleton-item"></div>
  </div>
  
  <div v-else>
    <!-- Contenido real -->
  </div>
</template>

<style>
.skeleton-item {
  height: 80px;
  background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
  border-radius: 8px;
  margin-bottom: 10px;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
```

#### Feedback Visual

```javascript
// Toast notifications
function showToast(message, type = 'success') {
  const toast = document.createElement('div')
  toast.className = `toast toast-${type}`
  toast.textContent = message
  
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.classList.add('fade-out')
    setTimeout(() => toast.remove(), 300)
  }, 3000)
}

// Uso
showToast('Incidencia creada con éxito', 'success')
showToast('Error al guardar', 'error')
```

---

## 🔌 APIs y Endpoints

### Autenticación

#### POST `/api/auth/register/`

**Request**

```json
{
  "email": "estudiante@uam.es",
  "password": "EstudianteUAM123$",
  "rol": "Estudiante",
  "telefono": "+34612345678"
}
```

**Response** (201 Created)

```json
{
  "id": 5,
  "email": "estudiante@uam.es",
  "username": "estudiante",
  "tipo": "normal",
  "rol": "Estudiante",
  "telefono": "+34612345678",
  "foto_perfil": null
}
```

**Errores**

```json
// 400 Bad Request
{
  "email": ["Usuario con este correo ya existe."],
  "password": ["La contraseña debe tener al menos 8 caracteres."]
}
```

#### POST `/api/auth/login/`

**Request**

```json
{
  "email": "operador@uam.es",
  "password": "Operador123$"
}
```

**Response** (200 OK)

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
  "user": {
    "id": 3,
    "email": "operador@uam.es",
    "username": "operador",
    "tipo": "seguridad",
    "rol": "Operador de Seguridad"
  }
}
```

#### POST `/api/auth/token/refresh/`

**Request**

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

**Response** (200 OK)

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Incidencias

#### GET `/api/incidencias/`

**Query Parameters**

```
?estado=pendiente              # Filtrar por estado
?tipo=robo                     # Filtrar por tipo
?usuario=5                     # Incidencias de un usuario
?fecha_desde=2026-01-01        # Rango de fechas
&fecha_hasta=2026-02-28
&ordering=-fecha_reporte       # Ordenar (- = descendente)
&search=laptop                 # Búsqueda en descripción
&page=2                        # Paginación
```

**Response** (200 OK)

```json
{
  "count": 156,
  "next": "http://localhost:8000/api/incidencias/?page=3",
  "previous": "http://localhost:8000/api/incidencias/?page=1",
  "results": [
    {
      "id": 42,
      "codigo_unico": "INC-2026-0042",
      "tipo": "robo",
      "descripcion": "Laptop robada de la biblioteca",
      "latitud": "40.548367",
      "longitud": "-3.687215",
      "direccion": "Biblioteca Central",
      "estado": "pendiente",
      "usuario": {
        "id": 5,
        "email": "estudiante@uam.es",
        "username": "estudiante"
      },
      "asignado_a": null,
      "fecha_reporte": "2026-02-28T10:30:00Z",
      "fecha_actualizacion": "2026-02-28T10:30:00Z",
      "archivos": [],
      "comentarios_count": 0
    }
  ]
}
```

#### POST `/api/incidencias/`

**Request** (multipart/form-data)

```
tipo: "robo"
descripcion: "Laptop robada de la biblioteca"
latitud: 40.548367
longitud: -3.687215
direccion: "Biblioteca Central, 2do piso"
archivos: [File, File]  # Opcional
```

**Response** (201 Created)

```json
{
  "id": 42,
  "codigo_unico": "INC-2026-0042",
  "tipo": "robo",
  "descripcion": "Laptop robada de la biblioteca",
  "latitud": "40.548367",
  "longitud": "-3.687215",
  "direccion": "Biblioteca Central, 2do piso",
  "estado": "pendiente",
  "usuario": 5,
  "asignado_a": null,
  "fecha_reporte": "2026-02-28T10:30:00Z",
  "archivos": [
    {
      "id": 10,
      "archivo": "/media/incidencias/2026/02/foto1.jpg",
      "tipo": "imagen",
      "descripcion": ""
    }
  ]
}
```

#### GET `/api/incidencias/{id}/`

**Response** (200 OK)

```json
{
  "id": 42,
  "codigo_unico": "INC-2026-0042",
  "tipo": "robo",
  "descripcion": "Laptop robada de la biblioteca",
  "latitud": "40.548367",
  "longitud": "-3.687215",
  "direccion": "Biblioteca Central",
  "estado": "pendiente",
  "usuario": {
    "id": 5,
    "email": "estudiante@uam.es",
    "username": "estudiante",
    "foto_perfil": "/media/avatars/estudiante.jpg"
  },
  "asignado_a": null,
  "fecha_reporte": "2026-02-28T10:30:00Z",
  "fecha_actualizacion": "2026-02-28T10:30:00Z",
  "nota_resolucion": null,
  "archivos": [
    {
      "id": 10,
      "archivo": "/media/incidencias/2026/02/foto1.jpg",
      "tipo": "imagen",
      "descripcion": ""
    }
  ],
  "comentarios": []
}
```

#### POST `/api/incidencias/{id}/cambiar_estado/`

**Request**

```json
{
  "estado": "resuelta",
  "nota_resolucion": "Laptop recuperada, se contactó al usuario"
}
```

**Response** (200 OK)

```json
{
  "id": 42,
  "codigo_unico": "INC-2026-0042",
  "estado": "resuelta",
  "nota_resolucion": "Laptop recuperada, se contactó al usuario",
  "fecha_actualizacion": "2026-03-01T14:20:00Z"
}
```

**Errores**

```json
// 403 Forbidden (permisos insuficientes)
{
  "detail": "No tienes permiso para realizar esta acción."
}

// 400 Bad Request (validación fallida)
{
  "nota_resolucion": ["Este campo es obligatorio para estado 'resuelta'."]
}
```

### Comentarios

#### POST `/api/comentarios/`

**Request**

```json
{
  "incidencia": 42,
  "texto": "Revisé la zona, no encontré evidencia"
}
```

**Response** (201 Created)

```json
{
  "id": 15,
  "texto": "Revisé la zona, no encontré evidencia",
  "usuario": {
    "id": 3,
    "email": "operador@uam.es",
    "username": "operador"
  },
  "incidencia": 42,
  "fecha_creacion": "2026-02-28T11:45:00Z",
  "editado": false
}
```

### Notificaciones

#### GET `/api/notificaciones/`

**Query Parameters**

```
?leida=false              # Solo no leídas
```

**Response** (200 OK)

```json
{
  "count": 3,
  "results": [
    {
      "id": 8,
      "tipo": "cambio_estado",
      "mensaje": "Tu incidencia INC-2026-0042 ha sido cambiada a 'En Proceso'",
      "leida": false,
      "fecha_creacion": "2026-02-28T12:00:00Z",
      "incidencia": 42
    }
  ]
}
```

#### POST `/api/notificaciones/{id}/marcar_leida/`

**Response** (200 OK)

```json
{
  "id": 8,
  "leida": true
}
```

### Alertas (Solo Staff)

#### POST `/api/alertas/`

**Request**

```json
{
  "incidencia": 42,
  "usuario": 5,
  "mensaje": "ALERTA: Situación potencialmente peligrosa detectada"
}
```

**Response** (201 Created)

```json
{
  "id": 3,
  "incidencia": 42,
  "usuario": 5,
  "mensaje": "ALERTA: Situación potencialmente peligrosa detectada",
  "estado": "pendiente",
  "fecha_creacion": "2026-02-28T13:00:00Z"
}
```

---

## 🔒 Seguridad

### Autenticación JWT

**Configuración Django**

```python
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

**Interceptor de Axios (Frontend)**

```javascript
// config/api.js
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor de Request (añadir token)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Interceptor de Response (refresh token)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    // Si es 401 y no es retry, intentar refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const refreshToken = localStorage.getItem('refresh')
      if (refreshToken) {
        try {
          const response = await axios.post('/api/auth/token/refresh/', {
            refresh: refreshToken
          })
          
          const newToken = response.data.access
          localStorage.setItem('token', newToken)
          
          // Reintentar request original con nuevo token
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return api(originalRequest)
        } catch (refreshError) {
          // Refresh falló, logout
          const authStore = useAuthStore()
          authStore.logout()
          return Promise.reject(refreshError)
        }
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
```

### CORS (Cross-Origin Resource Sharing)

**Backend**

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Producción (ejemplo con Vercel)
# CORS_ALLOWED_ORIGINS = [
#     "https://campus-guardian.vercel.app",
# ]

CORS_ALLOW_CREDENTIALS = True
```

### Validación de Input

#### Backend (Django Serializers)

```python
# api/serializers.py
from rest_framework import serializers
from app_models.models import Usuario
import re

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    def validate_email(self, value):
        """Validar dominio @uam.es"""
        if not (value.endswith('@uam.es') or value.endswith('@estudiante.uam.es')):
            raise serializers.ValidationError(
                "El email debe ser del dominio @uam.es o @estudiante.uam.es"
            )
        return value.lower()
    
    def validate_password(self, value):
        """Validar complejidad de password"""
        if len(value) < 8:
            raise serializers.ValidationError("Mínimo 8 caracteres")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Debe contener mayúscula")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Debe contener minúscula")
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Debe contener número")
        
        if not re.search(r'[!@#$%^&*]', value):
            raise serializers.ValidationError("Debe contener carácter especial")
        
        return value
    
    def validate_telefono(self, value):
        """Validar formato de teléfono"""
        if not re.match(r'^\+\d{2,3}\d{9}$', value):
            raise serializers.ValidationError(
                "Formato: +XX123456789 (prefijo + 9 dígitos)"
            )
        return value
```

#### Frontend (Vue Composables)

```javascript
// utils/validators.js
export function validateEmail(email) {
  const regex = /^[^\s@]+@(uam\.es|estudiante\.uam\.es)$/
  return regex.test(email) || 'Email debe ser @uam.es o @estudiante.uam.es'
}

export function validatePassword(password) {
  if (password.length < 8) return 'Mínimo 8 caracteres'
  if (!/[A-Z]/.test(password)) return 'Debe contener mayúscula'
  if (!/[a-z]/.test(password)) return 'Debe contener minúscula'
  if (!/\d/.test(password)) return 'Debe contener número'
  if (!/[!@#$%^&*]/.test(password)) return 'Debe contener carácter especial'
  return true
}

// Uso en formulario
const errors = ref({})

function validateForm() {
  errors.value.email = validateEmail(formData.email)
  errors.value.password = validatePassword(formData.password)
  
  return !Object.values(errors.value).some(error => error !== true)
}
```

### Protección contra Ataques

#### SQL Injection

**Django ORM Prevención**

```python
# ❌ VULNERABLE (raw SQL)
Incidencia.objects.raw(f"SELECT * FROM incidencias WHERE id = {user_input}")

# ✅ SEGURO (ORM + parametros)
Incidencia.objects.filter(id=user_input)

# ✅ SEGURO (raw SQL con params)
Incidencia.objects.raw("SELECT * FROM incidencias WHERE id = %s", [user_input])
```

#### XSS (Cross-Site Scripting)

**Vue Escaping Automático**

```vue
<!-- ✅ SEGURO (Vue escapa HTML por defecto) -->
<p>{{ usuario.descripcion }}</p>

<!-- ❌ PELIGROSO (v-html sin sanitizar) -->
<p v-html="usuario.descripcion"></p>

<!-- ✅ SEGURO (v-html CON sanitización) -->
<p v-html="sanitizeHTML(usuario.descripcion)"></p>
```

```javascript
import DOMPurify from 'dompurify'

function sanitizeHTML(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  })
}
```

#### CSRF (Cross-Site Request Forgery)

**Django CSRF Protection**

```python
# settings.py
MIDDLEWARE = [
    # ...
    'django.middleware.csrf.CsrfViewMiddleware',
]

# Para API REST con JWT, se puede deshabilitar CSRF en endpoints API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

**Frontend (Axios)**

```javascript
// config/api.js
api.defaults.xsrfHeaderName = 'X-CSRFToken'
api.defaults.xsrfCookieName = 'csrftoken'
```

#### Rate Limiting

**Django Throttling**

```python
# api/views.py
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class IncidenciaViewSet(viewsets.ModelViewSet):
    throttle_classes = [UserRateThrottle]  # 100 requests/hora por usuario

    def get_throttles(self):
        if self.action == 'create':
            # Limitar creación de incidencias
            return [UserRateThrottle()]  # 20 requests/hora
        return super().get_throttles()

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/hour',       # Usuarios no autenticados
        'user': '100/hour',      # Usuarios autenticados
    }
}
```

### Hash de Passwords

**Django (PBKDF2)**

```python
# Django usa PBKDF2 por defecto con 600,000 iteraciones

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Alternativa más segura
]

# Creación automática de hash
user = Usuario.objects.create_user(
    email='test@uam.es',
    password='PlainTextPassword123$'  # Se hashea automáticamente
)

# Verificación
user.check_password('PlainTextPassword123$')  # True
```

**Resultado**

```
pbkdf2_sha256$600000$random_salt$hash_de_64_caracteres
```

---

## 🚀 Despliegue

### Despliegue Backend (Django)

#### Render.com (Recomendado para TFG)

**1. Configuración**

Crear `build.sh` en raíz:

```bash
#!/usr/bin/env bash
set -o errexit

cd app_seguridad
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Crear `Procfile`:

```
web: cd app_seguridad && gunicorn app_seguridad.wsgi:application
```

**2. Settings de Producción**

```python
# settings.py
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database (ejemplo con PostgreSQL en producción)
if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (usar S3 en producción)
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
```

**3. Variables de Entorno en Render**

```
SECRET_KEY=tu-clave-secreta-de-produccion
DEBUG=False
ALLOWED_HOSTS=campus-guardian.onrender.com
DATABASE_URL=postgresql://...
CORS_ALLOWED_ORIGINS=https://campus-guardian.vercel.app
```

### Despliegue Frontend (Vue)

#### Vercel (Recomendado)

**1. Configuración**

Crear `vercel.json` en `frontend/`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**2. Variables de Entorno en Vercel**

```
VITE_API_URL=https://campus-guardian.onrender.com/api
# El frontend no necesita la key de Gemini; se configura en backend como GEMINI_API_KEY
```

**3. Deploy**

```bash
# CLI
npm i -g vercel
vercel login
vercel --prod

# O conectar GitHub repo en https://vercel.com
```

### Alternativas

#### Railway.app (Backend + Frontend)

```yaml
# railway.toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "cd app_seguridad && gunicorn app_seguridad.wsgi"
healthcheckPath = "/api/health/"
```

#### Netlify (Solo Frontend)

```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## 📚 Trabajo Futuro

### Mejoras Planificadas

#### 1. Notificaciones en Tiempo Real (WebSockets)

**Tecnología**: Django Channels + Redis

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            f'user_{self.user.id}',
            self.channel_name
        )
        await self.accept()
    
    async def notification_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
```

**Beneficio**: Notificaciones instantáneas sin polling

#### 2. Análisis de Datos e IA

**Funcionalidades**

- **Mapa de Calor**: Zonas con más incidencias
- **Predicción de Incidencias**: ML para predecir tipos de incidencia por zona/hora
- **Clasificación Automática**: Gemini clasifica tipo de incidencia desde descripción
- **Análisis de Sentimiento**: Detectar incidencias críticas por tono del mensaje

**Tecnología**: TensorFlow.js (frontend) o scikit-learn (backend)

#### 3. Aplicación Móvil Nativa

**Tecnología**: React Native o Flutter

**Funcionalidades Adicionales**

- Notificaciones Push nativas
- Geolocalización en background
- Captura de foto/video optimizada

#### 4. Sistema de Archivos en la Nube

**Actual**: Media files en servidor (no escalable)

**Mejora**: AWS S3 o Cloudinary

```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'eu-west-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
```

#### 5. Autenticación con OAuth2

**Proveedores**: Google, Microsoft (cuentas UAM)

```javascript
// Usando Firebase Auth
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth'

async function loginWithGoogle() {
  const provider = new GoogleAuthProvider()
  const result = await signInWithPopup(auth, provider)
  
  // Enviar token a backend para crear/vincular usuario
  await api.post('/api/auth/google/', {
    token: result.user.accessToken
  })
}
```

#### 6. Panel de Estadísticas Avanzado

**Dashboard con Gráficos**

- Incidencias por mes/semana/día (Chart.js)
- Tipos de incidencia más comunes (barras)
- Tiempo promedio de resolución (línea)
- Mapa de calor de zonas peligrosas

**Tecnología**: Chart.js, D3.js

#### 7. Sistema de Roles Más Granular

**Actual**: 3 tipos (normal, seguridad, admin)

**Mejora**: Permisos específicos

```python
# Django Guardian (object-level permissions)
from guardian.shortcuts import assign_perm

assign_perm('cambiar_estado_incidencia', operador, incidencia)
assign_perm('asignar_operadores', jefe_seguridad)
```

### Limitaciones Conocidas

1. **Polling para Notificaciones**: No tiempo real (WebSockets requerido)
2. **Media Files Locales**: No escalable (migrar a S3)
3. **Sin Caducidad de Tokens**: Access tokens no se invalidan manualmente
4. **Sin Audit Log**: No se registran todas las acciones (crear modelo `AuditLog`)
5. **Sin Backup Automático**: DB debe respaldarse manualmente
6. **Sin Métricas de Rendimiento**: No hay Observability (Sentry, Datadog)

---

## 📄 Licencia y Contacto

### Licencia

Este proyecto es un Trabajo de Fin de Grado (TFG) para la Universidad Autónoma de Madrid (UAM).

**Uso Académico**: Permitido con atribución.

**Uso Comercial**: Requiere permiso del autor.

### Autor

**David Zurita Sánchez**

- **Email**: david.zurita@estudiante.uam.es
- **Universidad**: Universidad Autónoma de Madrid (UAM)
- **Curso**: 2025/2026
- **Titulación**: Ingeniería Informática

### Referencias

#### Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue 3 Documentation](https://vuejs.org/guide/introduction.html)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [Google Gemini API](https://ai.google.dev/docs)
- [Cypress Documentation](https://docs.cypress.io/)

#### Libros y Artículos

- "Django for Professionals" (William S. Vincent)
- "Vue.js 3 Cookbook" (Heitor Ramon Ribeiro)
- "RESTful Web API Patterns and Practices Cookbook" (Mike Amundsen)

---

## 🙏 Agradecimientos

- **Tutor del TFG**: [Nombre del tutor] por su guía y feedback
- **Universidad Autónoma de Madrid**: Por proporcionar el contexto y la motivación del proyecto
- **Comunidad Open Source**: Django, Vue.js, Leaflet y todas las librerías utilizadas
- **Google**: Por la API de Gemini con tier gratuito generoso

---

**¡Gracias por revisar Campus Guardian!** 🛡️

Si tienes preguntas o sugerencias, no dudes en contactar.

---

*Última actualización: Enero 2026*

<a href="https://www.flaticon.es/iconos-gratis/campana-de-notificacion" title="campana de notificación iconos">Campana de notificación iconos creados por Pixel perfect - Flaticon</a>

<a href="https://www.flaticon.es/iconos-gratis/alfiler" title="alfiler iconos">Alfiler iconos creados por Freepik - Flaticon</a>


<a href="https://www.flaticon.es/iconos-gratis/lista" title="lista iconos">Lista iconos creados por Kiranshastry - Flaticon</a>

<a href="https://www.flaticon.es/iconos-gratis/incremento" title="incremento iconos">Incremento iconos creados por meaicon - Flaticon</a>

<a href="https://www.flaticon.es/iconos-gratis/lista" title="lista iconos">Lista iconos creados por Freepik - Flaticon</a>
