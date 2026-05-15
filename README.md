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

## Requisitos

- Python 3.11 o superior
- Node.js 18 o superior
- npm

## Instalación

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app_seguridad
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Pruebas

Para ejecutar Cypress:

```bash
cd frontend
npm run test:e2e
```

Antes de lanzar los tests, asegúrate de tener arrancados el backend y el frontend en modo preview o desarrollo según la configuración del proyecto.

## Producción

La aplicación está disponible en: https://campus-guardian-flame.vercel.app/

## Licencia

Proyecto académico para el Trabajo de Fin de Grado.