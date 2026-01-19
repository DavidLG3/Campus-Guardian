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
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { getIconForIncident } from '@/utils/leafletIcons'
import { useIncidenciaStore } from '@/stores/incidencia'
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()
const router = useRouter()

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
            <p><strong>Estado:</strong> <span class="estado-${incidencia.estado}">${incidencia.estado}</span>  <strong>Fecha:</strong> ${formatDate(incidencia.fecha_creacion)}</p>
            ${incidencia.direccion ? `<p><strong>Dirección:</strong> ${incidencia.direccion}</p>` : ''}
            <button onclick="navigateToIncidencia(${incidencia.id})" class="ver-detalle">Ver detalles →</button>
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

// Función global para navegar desde el popup
function navigateToIncidencia(id) {
  router.push({ name: 'DetalleIncidencia', params: { id: id } })
}

// Hacer la función accesible globalmente
window.navigateToIncidencia = navigateToIncidencia

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
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.mapa-content {
  padding: 2rem;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

h1 {
  font-size: 42px;
  margin-bottom: 2rem;
  color: #fff;
  font-weight: 900;
  letter-spacing: -0.02em;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.map-container {
  background: #fff;
  border-radius: var(--radius-2xl, 20px);
  overflow: hidden;
  border: 2px solid var(--success, #00ff88);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  margin-bottom: 1.5rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

#map {
  height: 600px;
  width: 100%;
}

.map-controls {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
}

.btn-control {
  padding: 1rem 2rem;
  background: #fff;
  color: #000;
  border: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-control::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--info, #00ccff);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.btn-control:hover::before {
  width: 300px;
  height: 300px;
}

.btn-control:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .mapa-content {
    padding: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  #map {
    height: 70vh;
  }

  .map-controls {
    flex-direction: column;
  }

  .btn-control {
    width: 100%;
  }
}
</style>

<style>
/* Estilos globales para los popups de Leaflet */
.leaflet-popup-content-wrapper {
  background: #ffffff !important;
  border: 2px solid #e0e0e0 !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
  padding: 0 !important;
}

.leaflet-popup-content {
  margin: 0 !important;
  width: auto !important;
  background: #ffffff !important;
}

.leaflet-popup-tip {
  background: #ffffff !important;
  border-left: 2px solid #e0e0e0 !important;
  border-bottom: 2px solid #e0e0e0 !important;
}

.popup-content {
  padding: 1rem;
  min-width: 250px;
  background: #ffffff !important;
}

.popup-content h3 {
  margin: 0 0 1rem 0;
  color: #000;
  font-size: 18px;
  font-weight: 800;
  text-transform: capitalize;
  letter-spacing: -0.01em;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #e0e0e0;
}

.popup-content p {
  margin: 0.75rem 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.popup-content p strong {
  color: #000;
  font-weight: 700;
  display: inline-block;
  min-width: 90px;
}

.popup-content .estado-abierta {
  color: var(--warning, #ffcc00);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 12px;
}

.popup-content .estado-en_progreso {
  color: var(--info, #00ccff);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 12px;
}

.popup-content .estado-resuelta {
  color: var(--success, #00ff88);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 12px;
}

.popup-content .ver-detalle {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #000;
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  font-size: 13px;
  border: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  width: 100%;
}

.popup-content .ver-detalle:hover {
  background: #00ff88;
  color: #000;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.4);
  text-decoration: none;
}

</style>
