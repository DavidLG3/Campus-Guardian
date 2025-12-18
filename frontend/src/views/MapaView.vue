<template>
  <div class="mapa-view">
    <AppLayout>
      <div class="mapa-content">
        <h1>Mapa de Incidencias</h1>
        
        <div class="map-container">
          <div id="map" ref="mapRef"></div>
        </div>
        
        <div class="map-controls">
          <button @click="centerMap" class="btn-control">📍 Centrar Mapa</button>
          <button @click="refreshIncidencias" class="btn-control">🔄 Actualizar</button>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { getIconForIncident } from '@/utils/leafletIcons'
import { useIncidenciaStore } from '@/stores/incidencia'
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()

const mapRef = ref(null)
let map = null
let markersLayer = null

const defaultCenter = [40.5472, -3.6894] // Campus de Cantoblanco, UAM
const defaultZoom = 13

function initMap() {
  // Crear el mapa
  map = L.map(mapRef.value).setView(defaultCenter, defaultZoom)
  
  // Añadir capa de tiles de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
  
  // Crear capa para los marcadores
  markersLayer = L.layerGroup().addTo(map)
  
  // Cargar incidencias
  loadIncidencias()
}

async function loadIncidencias() {
  try {
    await incidenciaStore.fetchAll()
    addMarkersToMap()
  } catch (error) {
    console.error('Error cargando incidencias:', error)
    // No relanzar el error, solo loguearlo
  }
}

function addMarkersToMap() {
  // Limpiar marcadores existentes
  markersLayer.clearLayers()
  
  // Añadir marcador por cada incidencia
  incidenciaStore.incidencias.forEach(incidencia => {
    if (incidencia.latitud && incidencia.longitud) {
      const icon = getIconForIncident(incidencia.tipo)
      
      const marker = L.marker([incidencia.latitud, incidencia.longitud], { icon })
        .bindPopup(`
          <div class="popup-content">
            <h3>${incidencia.tipo}</h3>
            <p><strong>Descripción:</strong> ${incidencia.descripcion || 'Sin descripción'}</p>
            <p><strong>Estado:</strong> <span class="estado-${incidencia.estado}">${incidencia.estado}</span></p>
            <p><strong>Fecha:</strong> ${formatDate(incidencia.fecha_creacion)}</p>
            ${incidencia.direccion ? `<p><strong>Dirección:</strong> ${incidencia.direccion}</p>` : ''}
            <a href="#/incidencias/${incidencia.id}" class="ver-detalle">Ver detalles →</a>
          </div>
        `)
      
      markersLayer.addLayer(marker)
    }
  })
}

function centerMap() {
  if (map) {
    map.setView(defaultCenter, defaultZoom)
  }
}

async function refreshIncidencias() {
  await loadIncidencias()
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('es-ES')
}

onMounted(() => {
  // Pequeño delay para asegurar que el DOM está listo
  setTimeout(initMap, 100)
})

onUnmounted(() => {
  if (map) {
    map.remove()
  }
})
</script>

<style scoped>
.mapa-content {
  padding: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

.map-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

#map {
  height: 600px;
  width: 100%;
}

.map-controls {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-control {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-control:hover {
  opacity: 0.9;
}
</style>

<style>
/* Estilos globales para los popups de Leaflet */
.popup-content h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
  text-transform: capitalize;
}

.popup-content p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
}

.popup-content .estado-abierta {
  color: #856404;
  font-weight: 600;
}

.popup-content .estado-en_progreso {
  color: #084298;
  font-weight: 600;
}

.popup-content .estado-resuelta {
  color: #0f5132;
  font-weight: 600;
}

.popup-content .ver-detalle {
  display: inline-block;
  margin-top: 0.5rem;
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.popup-content .ver-detalle:hover {
  text-decoration: underline;
}
</style>
