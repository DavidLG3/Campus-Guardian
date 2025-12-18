# 🚀 API de App Seguridad - Documentación

## 📋 Endpoints Disponibles

### 🔐 Autenticación

#### 1. Obtener Token (Login)
```http
POST /api/token/
Content-Type: application/json

{
    "username": "usuario",
    "password": "contraseña"
}
```

**Respuesta exitosa:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### 2. Refrescar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

#### 3. Registrar Nuevo Usuario
```http
POST /api/register/
Content-Type: application/json

{
    "username": "nuevo_usuario",
    "email": "email@example.com",
    "password": "contraseña123",
    "password2": "contraseña123",
    "tipo": "normal",
    "rol": "Estudiante",
    "first_name": "Juan",
    "last_name": "Pérez"
}
```

---

### 👤 Usuarios

**Nota:** Todos los endpoints requieren autenticación (excepto register y token).
**Header requerido:** `Authorization: Bearer <access_token>`

#### 1. Ver Mi Perfil
```http
GET /api/usuarios/me/
```

#### 2. Ver Mis Incidencias
```http
GET /api/usuarios/mis_incidencias/
```

#### 3. Ver Mis Alertas
```http
GET /api/usuarios/mis_alertas/
```

#### 4. Listar Usuarios (Solo Admin)
```http
GET /api/usuarios/
```

#### 5. Ver Usuario Específico
```http
GET /api/usuarios/{id}/
```

#### 6. Actualizar Mi Perfil
```http
PUT /api/usuarios/{id}/
PATCH /api/usuarios/{id}/

{
    "email": "nuevo@email.com",
    "rol": "Profesor",
    "first_name": "Juan"
}
```

---

### 📋 Incidencias

#### 1. Listar Incidencias
```http
GET /api/incidencias/
```
- **Usuario normal:** Solo ve sus propias incidencias
- **Usuario de seguridad:** Ve todas las incidencias

#### 2. Crear Incidencia
```http
POST /api/incidencias/
Content-Type: application/json

{
    "titulo": "Robo en biblioteca",
    "descripcion": "Se reportó el robo de una laptop en la biblioteca central",
    "tipo": "robo",
    "latitud": "40.416775",
    "longitud": "-3.703790"
}
```

**Tipos disponibles:**
- `robo`
- `accidente`
- `incendio`
- `vandalismo`
- `situacion_incomoda`
- `estafa`
- `otro`

#### 3. Ver Detalle de Incidencia
```http
GET /api/incidencias/{id}/
```

#### 4. Actualizar Incidencia
```http
PUT /api/incidencias/{id}/
PATCH /api/incidencias/{id}/

{
    "titulo": "Título actualizado",
    "descripcion": "Descripción actualizada"
}
```

#### 5. Eliminar Incidencia
```http
DELETE /api/incidencias/{id}/
```

#### 6. Cambiar Estado (Solo Usuarios de Seguridad)
```http
POST /api/incidencias/{id}/cambiar_estado/

{
    "estado": "en_proceso"
}
```

**Estados disponibles:**
- `pendiente`
- `en_proceso`
- `resuelta`

#### 7. Filtrar por Tipo
```http
GET /api/incidencias/por_tipo/?tipo=robo
```

#### 8. Filtrar por Estado
```http
GET /api/incidencias/por_estado/?estado=pendiente
```

---

### 🔔 Alertas

**Nota:** Las alertas se crean automáticamente cuando se crea una incidencia.

#### 1. Listar Mis Alertas
```http
GET /api/alertas/
```

#### 2. Ver Alertas Pendientes
```http
GET /api/alertas/pendientes/
```

#### 3. Marcar Alerta como Leída
```http
POST /api/alertas/{id}/marcar_leida/
```

#### 4. Ver Detalle de Alerta
```http
GET /api/alertas/{id}/
```

---

## 🔧 Ejemplos de Uso con cURL

### Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Crear Incidencia
```bash
curl -X POST http://localhost:8000/api/incidencias/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <tu_token_aqui>" \
  -d '{
    "titulo": "Accidente en parking",
    "descripcion": "Choque menor en el parking norte",
    "tipo": "accidente",
    "latitud": "40.416775",
    "longitud": "-3.703790"
  }'
```

### Ver Mis Incidencias
```bash
curl -X GET http://localhost:8000/api/usuarios/mis_incidencias/ \
  -H "Authorization: Bearer <tu_token_aqui>"
```

---

## 📦 Paginación

Todas las listas están paginadas (10 elementos por página).

```http
GET /api/incidencias/?page=2
```

---

## ⚠️ Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Sin permisos
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 🎯 Flujo de Trabajo Típico

1. **Registrar usuario:** `POST /api/register/`
2. **Login:** `POST /api/token/` → Obtener access token
3. **Crear incidencia:** `POST /api/incidencias/` (con token)
4. **Ver alertas:** `GET /api/alertas/` (usuarios de seguridad)
5. **Cambiar estado:** `POST /api/incidencias/{id}/cambiar_estado/`

---

## 🚀 Para Probar la API

1. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

2. Visita: http://localhost:8000/api/

3. Usa herramientas como:
   - **Postman**
   - **Insomnia**
   - **Thunder Client** (extensión de VS Code)
   - **cURL** (línea de comandos)
