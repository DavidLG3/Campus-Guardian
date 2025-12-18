# Sistema de Seguridad - Aplicación Web

Sistema completo de gestión de seguridad con backend Django y frontend Vue.js.

## 🛠️ Tecnologías

### Backend
- Django 4.2
- Django REST Framework
- JWT Authentication
- SQLite (desarrollo)

### Frontend
- Vue 3
- Vite
- Pinia (State Management)
- Vue Router
- Axios
- Leaflet (Mapas)

## 📋 Requisitos Previos

- Python 3.8+
- Node.js 20.19+ o 22.12+
- npm

## 🚀 Instalación

### Backend (Django)

1. **Activar el entorno virtual:**
   ```bash
   cd /home/davizurius/Desktop/Cuarto_Carrera/TFG
   source venv/bin/activate
   ```

2. **Instalar dependencias (si es necesario):**
   ```bash
   pip install -r requirements.txt
   ```

3. **Aplicar migraciones:**
   ```bash
   cd app_seguridad
   python manage.py migrate
   ```

4. **Crear superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```

   El backend estará disponible en: `http://localhost:8000`

### Frontend (Vue.js)

1. **Navegar a la carpeta frontend:**
   ```bash
   cd /home/davizurius/Desktop/Cuarto_Carrera/TFG/frontend
   ```

2. **Instalar dependencias:**
   ```bash
   npm install
   ```

3. **Ejecutar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

   El frontend estará disponible en: `http://localhost:5173`

## 📁 Estructura del Proyecto

```
TFG/
├── app_seguridad/          # Backend Django
│   ├── api/                # Endpoints de la API REST
│   ├── app_models/         # Modelos de datos
│   ├── app_seguridad/      # Configuración del proyecto
│   └── manage.py
├── frontend/               # Frontend Vue.js
│   ├── src/
│   │   ├── components/     # Componentes reutilizables
│   │   ├── views/          # Vistas/Páginas
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # Servicios API
│   │   ├── router/         # Configuración de rutas
│   │   ├── layouts/        # Layouts de la aplicación
│   │   └── config/         # Configuración
│   └── package.json
└── venv/                   # Entorno virtual Python
```

## 🔑 Funcionalidades Principales

### Autenticación
- ✅ Registro de usuarios
- ✅ Login con JWT
- ✅ Protección de rutas
- ✅ Gestión de perfiles

### Incidencias
- ✅ Listar incidencias
- ✅ Crear nueva incidencia
- ✅ Ver detalles de incidencia
- ✅ Cambiar estado (admin/operador)
- ✅ Geolocalización con coordenadas
- ✅ Visualización en mapa

### Alertas
- ✅ Listar alertas
- ✅ Crear alertas (admin/operador)
- ✅ Filtrar por nivel/estado
- ✅ Marcar como leída
- ✅ Notificaciones visuales

### Mapa Interactivo
- ✅ Visualización de incidencias en mapa
- ✅ Marcadores por tipo de incidencia
- ✅ Popups con información
- ✅ Integración con Leaflet/OpenStreetMap

## 👥 Roles de Usuario

1. **Ciudadano**: Puede reportar incidencias y ver alertas
2. **Operador**: Puede gestionar incidencias y crear alertas
3. **Administrador**: Acceso completo al sistema

## 🌐 Endpoints de la API

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/register/` - Registrar usuario
- `POST /api/auth/logout/` - Cerrar sesión
- `GET /api/auth/user/` - Obtener usuario actual

### Incidencias
- `GET /api/incidencias/` - Listar incidencias
- `POST /api/incidencias/` - Crear incidencia
- `GET /api/incidencias/{id}/` - Detalle de incidencia
- `PUT /api/incidencias/{id}/` - Actualizar incidencia
- `PATCH /api/incidencias/{id}/` - Actualización parcial
- `DELETE /api/incidencias/{id}/` - Eliminar incidencia

### Alertas
- `GET /api/alertas/` - Listar alertas
- `POST /api/alertas/` - Crear alerta
- `GET /api/alertas/{id}/` - Detalle de alerta
- `PUT /api/alertas/{id}/` - Actualizar alerta
- `PATCH /api/alertas/{id}/` - Actualización parcial
- `DELETE /api/alertas/{id}/` - Eliminar alerta

### Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `GET /api/usuarios/{id}/` - Detalle de usuario
- `PUT /api/usuarios/{id}/` - Actualizar usuario

## 🔧 Variables de Entorno

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

### Backend
Las configuraciones están en `app_seguridad/app_seguridad/settings.py`

## 📝 Notas de Desarrollo

- El backend debe estar ejecutándose antes de usar el frontend
- CORS está configurado para permitir peticiones desde `localhost:5173`
- Los tokens JWT tienen una duración de 5 horas
- La base de datos SQLite se crea automáticamente al ejecutar las migraciones

## 🐛 Solución de Problemas

### Error de CORS
Si aparecen errores de CORS, verifica que:
- `django-cors-headers` esté instalado
- El middleware CORS esté configurado en `settings.py`
- La URL del frontend esté en `CORS_ALLOWED_ORIGINS`

### Error de conexión con la API
- Verifica que el backend esté ejecutándose en `localhost:8000`
- Revisa que la variable `VITE_API_URL` esté correctamente configurada

### Problemas con npm install
Si `npm install` se queda colgado:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 📄 Licencia

Este proyecto es parte de un Trabajo de Fin de Grado (TFG).
