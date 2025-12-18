# 🗺️ Integración con Leaflet - Guía del Backend

## ✅ Cambios Realizados en el Backend

### 1. **Modelo Incidencia actualizado**

Se han mejorado los campos de ubicación:

```python
# Coordenadas obligatorias con validación
latitud = models.DecimalField(
    max_digits=9, 
    decimal_places=6,
    default=0.0,
    validators=[MinValueValidator(-90), MaxValueValidator(90)]
)

longitud = models.DecimalField(
    max_digits=9, 
    decimal_places=6,
    default=0.0,
    validators=[MinValueValidator(-180), MaxValueValidator(180)]
)

# Campo adicional para dirección legible
direccion = models.CharField(max_length=300, blank=True, default='')
```

**Mejoras:**
- ✅ Validación de rangos válidos (lat: -90 a 90, lon: -180 a 180)
- ✅ Campo `direccion` para texto descriptivo (ej: "Biblioteca Central, 2do piso")
- ✅ Valores por defecto para migración sin problemas

---

### 2. **Nuevo Endpoint GeoJSON para Mapas**

#### `GET /api/incidencias/mapa/`

Devuelve todas las incidencias en formato **GeoJSON** estándar, ideal para Leaflet.

**Ejemplo de respuesta:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-3.703790, 40.416775]
      },
      "properties": {
        "id": 1,
        "titulo": "Robo en biblioteca",
        "descripcion": "Se reportó el robo de una laptop",
        "tipo": "robo",
        "estado": "pendiente",
        "direccion": "Biblioteca Central, 2do piso",
        "fecha_reporte": "2025-10-23T14:30:00Z",
        "usuario": "juan123"
      }
    }
  ]
}
```

**Uso en Leaflet:**
```javascript
// Cargar incidencias en el mapa
fetch('http://localhost:8000/api/incidencias/mapa/', {
    headers: {
        'Authorization': 'Bearer ' + token
    }
})
.then(response => response.json())
.then(data => {
    L.geoJSON(data, {
        onEachFeature: function(feature, layer) {
            layer.bindPopup(`
                <b>${feature.properties.titulo}</b><br>
                ${feature.properties.descripcion}<br>
                <small>Estado: ${feature.properties.estado}</small>
            `);
        }
    }).addTo(map);
});
```

---

### 3. **Serializers actualizados**

Los serializers ahora incluyen el campo `direccion`:

**Para crear incidencia:**
```json
POST /api/incidencias/
{
    "titulo": "Accidente en parking",
    "descripcion": "Choque menor",
    "tipo": "accidente",
    "latitud": 40.416775,
    "longitud": -3.703790,
    "direccion": "Parking Norte, cerca de la entrada principal"
}
```

---

## 🎯 Flujo de Trabajo con Leaflet

### **Para el Usuario Normal (Crear Alerta):**

1. **Mostrar mapa con Leaflet**
2. **Usuario hace clic en el mapa** → captura coordenadas
3. **Usuario completa formulario** con título, descripción, tipo
4. **Enviar POST** a `/api/incidencias/`:
   ```javascript
   const data = {
       titulo: "Robo de bicicleta",
       descripcion: "Reporto robo de bicicleta",
       tipo: "robo",
       latitud: marker.getLatLng().lat,
       longitud: marker.getLatLng().lng,
       direccion: "Parking de bicicletas, Facultad de Ciencias"
   };
   ```

### **Para Personal de Seguridad (Ver Alertas):**

1. **Cargar mapa con Leaflet**
2. **Hacer GET** a `/api/incidencias/mapa/`
3. **Renderizar marcadores** en el mapa con los datos GeoJSON
4. **Mostrar popups** al hacer clic en marcadores
5. **Opciones adicionales:**
   - Filtrar por tipo: `GET /api/incidencias/por_tipo/?tipo=robo`
   - Filtrar por estado: `GET /api/incidencias/por_estado/?estado=pendiente`

---

## 📝 Ejemplo Completo de Integración Frontend

### HTML básico con Leaflet:

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="height: 600px;"></div>
    
    <script>
        // Inicializar mapa (ejemplo: Madrid)
        const map = L.map('map').setView([40.416775, -3.703790], 13);
        
        // Agregar capa de OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
        
        // Cargar incidencias
        const token = localStorage.getItem('access_token');
        
        fetch('http://localhost:8000/api/incidencias/mapa/', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                pointToLayer: function(feature, latlng) {
                    // Diferentes colores según tipo
                    const colors = {
                        'robo': 'red',
                        'accidente': 'orange',
                        'incendio': 'darkred',
                        'vandalismo': 'purple',
                        'situacion_incomoda': 'yellow',
                        'estafa': 'blue',
                        'otro': 'gray'
                    };
                    
                    return L.circleMarker(latlng, {
                        radius: 8,
                        fillColor: colors[feature.properties.tipo] || 'gray',
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                },
                onEachFeature: function(feature, layer) {
                    const props = feature.properties;
                    layer.bindPopup(`
                        <div>
                            <h3>${props.titulo}</h3>
                            <p>${props.descripcion}</p>
                            <p><b>Tipo:</b> ${props.tipo}</p>
                            <p><b>Estado:</b> ${props.estado}</p>
                            ${props.direccion ? `<p><b>Ubicación:</b> ${props.direccion}</p>` : ''}
                            <p><small>Reportado: ${new Date(props.fecha_reporte).toLocaleString()}</small></p>
                            <p><small>Por: ${props.usuario}</small></p>
                        </div>
                    `);
                }
            }).addTo(map);
        });
        
        // Para crear nueva incidencia: capturar clic
        let marker;
        map.on('click', function(e) {
            if (marker) map.removeLayer(marker);
            marker = L.marker(e.latlng).addTo(map);
            
            // Guardar coordenadas para el formulario
            document.getElementById('latitud').value = e.latlng.lat;
            document.getElementById('longitud').value = e.latlng.lng;
        });
    </script>
</body>
</html>
```

---

## 🚀 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/incidencias/` | Lista de incidencias (JSON normal) |
| GET | `/api/incidencias/mapa/` | **Incidencias en formato GeoJSON** |
| POST | `/api/incidencias/` | Crear incidencia con coordenadas |
| GET | `/api/incidencias/{id}/` | Detalle de incidencia |
| GET | `/api/incidencias/por_tipo/?tipo=robo` | Filtrar por tipo |
| GET | `/api/incidencias/por_estado/?estado=pendiente` | Filtrar por estado |

---

## 💡 Consejos

1. **Geocoding inverso**: Puedes usar APIs como Nominatim para convertir coordenadas a dirección:
   ```javascript
   fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
   ```

2. **Clustering**: Para muchas incidencias, usa [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster)

3. **Iconos personalizados**: Crea iconos diferentes para cada tipo de incidencia

4. **Tiempo real**: Considera usar WebSockets para actualizar el mapa en tiempo real

---

¡El backend está listo para integrar con Leaflet! 🎉
