<template>
  <div class="detalle-incidencia-view">
    <AppLayout>
      <div class="detalle-content">
        <div v-if="isLoading" class="loading">Cargando...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-else-if="incidencia" class="incidencia-detalle">
          <div class="header-section">
            <div class="header-left">
              <h1 class="codigo-principal-detalle">{{ incidencia.codigo_unico }}</h1>
              <span class="tipo-badge-detalle">{{ formatTipo(incidencia.tipo) }}</span>
            </div>
            <span :class="['estado-badge', incidencia.estado]">
              {{ formatEstado(incidencia.estado) }}
            </span>
          </div>
          
          <div class="content-grid">
            <div class="main-info">
              <div class="info-card">
                <h2>Descripción</h2>
                <p>{{ incidencia.descripcion || 'Sin descripción' }}</p>
              </div>
              
              <div class="info-card">
                <h2>Información General</h2>
                <div class="info-list">
                  <div class="info-item">
                    <strong>Fecha de Reporte:</strong>
                    <span>{{ formatDate(incidencia.fecha_creacion) }}</span>
                  </div>
                  
                  <div v-if="incidencia.direccion" class="info-item">
                    <strong>Dirección:</strong>
                    <span>{{ incidencia.direccion }}</span>
                  </div>
                  
                  <div v-if="incidencia.latitud && incidencia.longitud" class="info-item">
                    <strong>Coordenadas:</strong>
                    <span>{{ incidencia.latitud }}, {{ incidencia.longitud }}</span>
                  </div>
                  
                  <div v-if="incidencia.usuario_reporta" class="info-item">
                    <strong>Reportado por:</strong>
                    <span>{{ incidencia.usuario_reporta.nombre }}</span>
                  </div>
                  
                  <div v-if="incidencia.usuario_asignado" class="info-item">
                    <strong>Asignado a:</strong>
                    <span>{{ incidencia.usuario_asignado.nombre }}</span>
                  </div>
                </div>
              </div>
              
              <div v-if="canChangeStatus" class="info-card">
                <h2>Gestión de Incidencia</h2>
                
                <!-- Cambiar estado -->
                <div class="status-actions">
                  <button
                    v-if="incidencia.estado !== 'abierta'"
                    @click="cambiarEstado('abierta')"
                    class="btn-status btn-abierta"
                  >
                    Marcar como Abierta
                  </button>
                  <button
                    v-if="incidencia.estado !== 'en_progreso'"
                    @click="cambiarEstado('en_progreso')"
                    :disabled="isAsignadaAOtro"
                    class="btn-status btn-en-progreso"
                    :title="isAsignadaAOtro ? `Ya está siendo atendida por ${incidencia.usuario_asignado?.nombre}` : ''"
                  >
                    Marcar como En Progreso
                  </button>
                </div>
                
                <!-- Mensaje si está asignada a otro -->
                <div v-if="isAsignadaAOtro" class="warning-message">
                  ⚠️ Esta incidencia está siendo atendida por {{ incidencia.usuario_asignado.nombre }}
                </div>
                
                <!-- Resolver incidencia -->
                <div v-if="incidencia.estado !== 'resuelta'" class="resolver-section">
                  <h3>Resolver Incidencia</h3>
                  <textarea
                    v-model="notaResolucion"
                    placeholder="Escribe una breve descripción de cómo se resolvió la incidencia..."
                    rows="4"
                    class="nota-textarea"
                  ></textarea>
                  <button
                    @click="resolverIncidencia"
                    :disabled="!notaResolucion.trim()"
                    class="btn-status btn-resolver"
                  >
                    ✓ Marcar como Resuelta
                  </button>
                </div>
              </div>
              
              <!-- Mostrar información de resolución si está resuelta -->
              <div v-if="incidencia.estado === 'resuelta' && incidencia.nota_resolucion" class="info-card resolucion-card">
                <h2>Resolución</h2>
                <div class="info-list">
                  <div class="info-item">
                    <strong>Nota:</strong>
                    <p>{{ incidencia.nota_resolucion }}</p>
                  </div>
                  <div v-if="incidencia.fecha_resolucion" class="info-item">
                    <strong>Fecha de Resolución:</strong>
                    <span>{{ formatDate(incidencia.fecha_resolucion) }}</span>
                  </div>
                  <div v-if="incidencia.resuelto_por_nombre" class="info-item">
                    <strong>Resuelto por:</strong>
                    <span>{{ incidencia.resuelto_por_nombre.nombre }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="incidencia.latitud && incidencia.longitud" class="sidebar">
              <div class="map-card">
                <h2>Ubicación</h2>
                <div id="detail-map" ref="mapRef"></div>
                <a
                  :href="`https://www.google.com/maps?q=${incidencia.latitud},${incidencia.longitud}`"
                  target="_blank"
                  class="btn-map-external"
                >
                  Abrir en Google Maps →
                </a>
              </div>
            </div>
          </div>
          
          <div class="actions-section">
            <router-link to="/incidencias" class="btn-back">
              ← Volver a Incidencias
            </router-link>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useIncidenciaStore } from '@/stores/incidencia'
import { useAuthStore } from '@/stores/auth'
import { useAlertaStore } from '@/stores/alerta'
import AppLayout from '@/layouts/AppLayout.vue'

const route = useRoute()
const router = useRouter()
const incidenciaStore = useIncidenciaStore()
const authStore = useAuthStore()
const alertaStore = useAlertaStore()

const incidencia = ref(null)
const isLoading = ref(false)
const error = ref('')
const notaResolucion = ref('')
const mapRef = ref(null)
let map = null

const canChangeStatus = computed(() => 
  authStore.isAdmin || authStore.isOperador
)

const isAsignadaAOtro = computed(() => {
  if (!incidencia.value?.usuario_asignado) return false
  return incidencia.value.usuario_asignado.id !== authStore.user?.id
})

function formatEstado(estado) {
  const estados = {
    'abierta': 'Abierta',
    'en_progreso': 'En Progreso',
    'resuelta': 'Resuelta'
  }
  return estados[estado] || estado
}

function formatTipo(tipo) {
  const tipos = {
    'robo': 'Robo',
    'accidente': 'Accidente',
    'incendio': 'Incendio',
    'vandalismo': 'Vandalismo',
    'situacion_incomoda': 'Situación Incómoda',
    'estafa': 'Estafa',
    'otro': 'Otro'
  }
  return tipos[tipo] || tipo
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleString('es-ES', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function cambiarEstado(nuevoEstado) {
  try {
    const resultado = await incidenciaStore.updateEstado(incidencia.value.id, nuevoEstado)
    incidencia.value = resultado
    error.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al cambiar el estado'
  }
}

async function resolverIncidencia() {
  if (!notaResolucion.value.trim()) {
    error.value = 'Debe proporcionar una nota de resolución'
    return
  }
  
  try {
    const resultado = await incidenciaStore.resolver(incidencia.value.id, notaResolucion.value)
    incidencia.value = resultado
    notaResolucion.value = ''
    // Recargar alertas para actualizar el contador en el navbar
    if (authStore.isAdmin || authStore.isOperador) {
      await alertaStore.fetchAll()
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al resolver la incidencia'
  }
}

function initMap() {
  if (!incidencia.value?.latitud || !incidencia.value?.longitud) return
  
  if (mapRef.value) {
    map = L.map(mapRef.value).setView(
      [incidencia.value.latitud, incidencia.value.longitud],
      15
    )
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)
    
    L.marker([incidencia.value.latitud, incidencia.value.longitud])
      .addTo(map)
      .bindPopup(incidencia.value.tipo)
      .openPopup()
  }
}

onMounted(async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const id = route.params.id
    const data = await incidenciaStore.fetchById(id)
    incidencia.value = data
    
    // Inicializar mapa después de cargar los datos
    setTimeout(initMap, 100)
  } catch (err) {
    console.error('Error al cargar la incidencia:', err)
    error.value = 'Error al cargar la incidencia. Puede que no exista o no tengas permisos.'
  } finally {
    isLoading.value = false
  }
})

onUnmounted(() => {
  if (map) {
    map.remove()
  }
})
</script>

<style scoped>
.detalle-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.error {
  color: #dc3545;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header-section .header-left {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.codigo-principal-detalle {
  font-size: 2.5rem;
  color: #1976d2;
  margin: 0;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.tipo-badge-detalle {
  display: inline-block;
  width: fit-content;
  padding: 0.35rem 0.9rem;
  background-color: #f5f5f5;
  color: #666;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
}

.estado-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
}

.estado-badge.abierta {
  background-color: #fff3cd;
  color: #856404;
}

.estado-badge.en_progreso {
  background-color: #cfe2ff;
  color: #084298;
}

.estado-badge.resuelta {
  background-color: #d1e7dd;
  color: #0f5132;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.main-info, .sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card, .map-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 1.25rem;
  color: #333;
  margin: 0 0 1rem 0;
}

.info-card p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item strong {
  color: #666;
  font-weight: 600;
}

.info-item span {
  color: #333 !important;
  font-weight: 400;
}

.info-item p {
  color: #333 !important;
  margin: 0;
}

.status-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.btn-status {
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-status:hover {
  opacity: 0.9;
}

.btn-abierta {
  background-color: #ffc107;
  color: #333;
}

.btn-en-progreso {
  background-color: #0dcaf0;
  color: white;
}

.btn-resuelta {
  background-color: #198754;
  color: white;
}

.resolver-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f0f0f0;
}

.resolver-section h3 {
  font-size: 1.1rem;
  color: #333;
  margin-bottom: 1rem;
}

.nota-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  margin-bottom: 0.75rem;
}

.nota-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.btn-resolver {
  background-color: #198754;
  color: white;
  width: 100%;
}

.btn-resolver:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.6;
}

.btn-en-progreso:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.5;
}

.warning-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  border-radius: 4px;
  color: #856404;
  font-size: 0.9rem;
}

.resolucion-card {
  background-color: #d1e7dd;
  border-left: 4px solid #198754;
}

.resolucion-card .info-item p {
  margin-top: 0.5rem;
  font-style: italic;
}

#detail-map {
  height: 300px;
  width: 100%;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.btn-map-external {
  display: block;
  text-align: center;
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.btn-map-external:hover {
  text-decoration: underline;
}

.actions-section {
  display: flex;
  justify-content: space-between;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-back:hover {
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .detalle-content {
    padding: 1rem;
  }

  .codigo-principal-detalle {
    font-size: 1.75rem;
  }

  .tipo-badge-detalle {
    font-size: 0.85rem;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .info-card,
  .map-card {
    padding: 1rem;
  }

  h2 {
    font-size: 1.1rem;
  }

  #detail-map {
    height: 250px;
  }
}

@media (max-width: 480px) {
  .detalle-content {
    padding: 0.75rem;
  }

  .codigo-principal-detalle {
    font-size: 1.5rem;
  }

  .estado-badge {
    font-size: 0.8rem;
    padding: 0.35rem 0.75rem;
  }

  .btn-status {
    font-size: 0.85rem;
    padding: 0.6rem 1rem;
  }

  .nota-textarea {
    font-size: 0.9rem;
  }

  .btn-back {
    width: 100%;
    text-align: center;
  }
}
</style>
