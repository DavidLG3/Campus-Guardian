<template>
  <div class="mapa-view">
    <AppLayout>
      <div class="mapa-content">
        <h1>Mapa de Incidencias</h1>
        
        <!-- Windows -->
        <div class="tabs-container">
          <button 
            :class="['tab-btn', { active: activeTab === 'activas' }]" 
            @click="activeTab = 'activas'"
          >
            📍 Incidencias Activas
          </button>
          <button 
            :class="['tab-btn', { active: activeTab === 'historial' }]" 
            @click="activeTab = 'historial'"
          >
            📚 Historial
          </button>
        </div>
        
        <!-- Filter by type -->
        <div class="filter-container">
          <label for="tipo-filter">Filtrar por tipo:</label>
          <select id="tipo-filter" v-model="filtroTipo" class="filter-select">
            <option value="">Todos los tipos</option>
            <option value="robo">Robo</option>
            <option value="vandalismo">Vandalismo</option>
            <option value="accidente">Accidente</option>
            <option value="incendio">Incendio</option>
            <option value="situacion_incomoda">Situación Incómoda</option>
            <option value="estafa">Estafa</option>
            <option value="otro">Otro</option>
          </select>
        </div>
        
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
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { getIconForIncident } from '@/utils/leafletIcons'
import { useIncidenciaStore } from '@/stores/incidencia'
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()
const router = useRouter()

const mapRef = ref(null)
const activeTab = ref('activas')
const filtroTipo = ref('')
let map = null
let markersLayer = null

const defaultCenter = [40.5472, -3.6894] // Campus de Cantoblanco, UAM
const defaultZoom = 13

// Computed to filter incidents according to active tab and filter
const incidenciasFiltradas = computed(() => {
  let incidencias = []
  
  if (activeTab.value === 'activas') {
    // Show open and ongoing issues
    incidencias = incidenciaStore.incidencias.filter(i => 
      i.estado === 'abierta' || i.estado === 'en_progreso'
    )
  } else {
    // Show resolved issues
    incidencias = incidenciaStore.incidencias.filter(i => i.estado === 'resuelta')
  }
  
  // Apply filter by type if selected
  if (filtroTipo.value) {
    incidencias = incidencias.filter(i => i.tipo === filtroTipo.value)
  }
  
  return incidencias
})

// Watch to update bookmarks when the filter or tab changes
watch([activeTab, filtroTipo, () => incidenciaStore.incidencias], () => {
  addMarkersToMap()
}, { deep: true })

function initMap() {
  // Create the map
  map = L.map(mapRef.value).setView(defaultCenter, defaultZoom)
  
  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
  
  markersLayer = L.layerGroup().addTo(map)
  
  loadIncidencias()
}

async function loadIncidencias() {
  try {
    await incidenciaStore.fetchAll()
    addMarkersToMap()
  } catch (error) {
    console.error('Error cargando incidencias:', error)
  }
}

function addMarkersToMap() {
  markersLayer.clearLayers()
  
  // Add marker for each filtered incident
  incidenciasFiltradas.value.forEach(incidencia => {
    if (incidencia.latitud && incidencia.longitud) {
      const icon = getIconForIncident(incidencia.tipo)
      
      const marker = L.marker([incidencia.latitud, incidencia.longitud], { icon })
        .bindPopup(`
          <div class="popup-content">
            <h3>${formatTipo(incidencia.tipo)}</h3>
            <p><strong>Descripción:</strong> ${incidencia.descripcion || 'Sin descripción'}</p>
            <p><strong>Estado:</strong> <span class="estado-${incidencia.estado}">${formatEstado(incidencia.estado)}</span></p>
            <p><strong>Fecha:</strong> ${formatDate(incidencia.fecha_creacion)}</p>
            ${incidencia.ubicacion ? `<p><strong>Ubicación:</strong> ${incidencia.ubicacion}</p>` : ''}
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

function formatEstado(estado) {
  const estados = {
    'abierta': 'Pendiente',
    'en_progreso': 'En Proceso',
    'resuelta': 'Resuelta'
  }
  return estados[estado] || estado
}

function formatTipo(tipo) {
  const tipos = {
    'robo': 'Robo',
    'vandalismo': 'Vandalismo',
    'accidente': 'Accidente',
    'incendio': 'Incendio',
    'situacion_incomoda': 'Situación Incómoda',
    'estafa': 'Estafa',
    'otro': 'Otro'
  }
  return tipos[tipo] || tipo
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('es-ES')
}

// Global function to navigate from the popup
function navigateToIncidencia(id) {
  router.push({ name: 'DetalleIncidencia', params: { id: id } })
}

// Make the function globally accessible
window.navigateToIncidencia = navigateToIncidencia

onMounted(() => {
  // A small delay to ensure the DOM is ready
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
  padding: 3.5rem 2rem 2rem;
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

.tabs-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

.tab-btn {
  flex: 1;
  padding: 1rem 2rem;
  background: #222;
  color: #fff;
  border: 2px solid #333;
  border-radius: var(--radius-lg, 12px);
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn:hover {
  background: #333;
  border-color: #00ff88;
}

.tab-btn.active {
  background: #00ff88;
  color: #000;
  border-color: #00ff88;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.3);
}

.filter-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.15s backwards;
}

.filter-container label {
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.filter-select {
  flex: 1;
  padding: 0.75rem 1.25rem;
  background: #222;
  color: #fff;
  border: 2px solid #333;
  border-radius: var(--radius-lg, 12px);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:hover {
  border-color: #00ff88;
}

.filter-select:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1);
}

.filter-select option {
  background: #222;
  color: #fff;
}

.map-container {
  background: #fff;
  border-radius: var(--radius-2xl, 20px);
  overflow: hidden;
  border: 2px solid var(--success, #00ff88);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  margin-bottom: 1.5rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
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

  .tabs-container {
    flex-direction: column;
  }

  .tab-btn {
    width: 100%;
  }

  .filter-container {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-container label {
    text-align: left;
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
/* Global styles for Leaflet popups */
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
