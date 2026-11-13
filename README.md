# Campus Guardian

Campus Guardian es una aplicación web para gestionar incidencias de seguridad en un entorno universitario. Permite a los usuarios registrar incidencias, seguir su estado y consultar información básica del sistema desde una interfaz web y una API REST.

## Proyecto

- Frontend: Vue 3 + Vite
- Backend: Django + Django REST Framework
- Base de datos: SQLite en desarrollo
- Testing E2E: Cypress

## Funcionalidades principales

- Registro e inicio de sesión de usuarios
- Creación y seguimiento de incidencias
- Gestión de incidencias por parte del personal autorizado
- Visualización de incidencias en mapa
- Sistema de comentarios y notificaciones
- Limpieza automática de datos de prueba en Cypress

## Estructura

- `app_seguridad/`: backend Django
- `frontend/`: aplicación Vue
- `requirements.txt`: dependencias del backend
- `frontend/package.json`: dependencias del frontend

## Producción

La aplicación está disponible en: https://campus-guardian-flame.vercel.app/
Si se obtienen errores en el login o registro, debe esperar unos minutos hasta que se termine de activar el servidor Render que posee el backend.

## Licencia

Proyecto académico para el Trabajo de Fin de Grado.
