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
import { getIconForIncident } from '@/utils/leafletIcons'
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
    
    const icon = getIconForIncident(incidencia.value.tipo)
    
    L.marker([incidencia.value.latitud, incidencia.value.longitud], { icon })
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
  }
}

.detalle-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

.loading, .error {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 18px;
  font-weight: 600;
  animation: fadeIn 0.4s ease;
}

.error {
  color: var(--error, #ff4444);
  background: rgba(255, 68, 68, 0.1);
  border-radius: var(--radius-xl, 16px);
  border: 2px solid rgba(255, 68, 68, 0.3);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.header-section .header-left {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.codigo-principal-detalle {
  font-size: 48px;
  color: #fff;
  margin: 0;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.tipo-badge-detalle {
  display: inline-block;
  width: fit-content;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-radius: var(--radius-full, 9999px);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.estado-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full, 9999px);
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 2px solid;
}

.estado-badge.abierta {
  background: rgba(255, 204, 0, 0.2);
  color: var(--warning, #ffcc00);
  border-color: var(--warning, #ffcc00);
}

.estado-badge.en_progreso {
  background: rgba(0, 204, 255, 0.2);
  color: var(--info, #00ccff);
  border-color: var(--info, #00ccff);
}

.estado-badge.resuelta {
  background: rgba(0, 255, 136, 0.2);
  color: var(--success, #00ff88);
  border-color: var(--success, #00ff88);
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
  background: #fff;
  border: 2px solid var(--success, #00ff88);
  border-radius: var(--radius-xl, 16px);
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.info-card:nth-child(1) { animation-delay: 0.1s; }
.info-card:nth-child(2) { animation-delay: 0.2s; }
.info-card:nth-child(3) { animation-delay: 0.3s; }
.info-card:nth-child(4) { animation-delay: 0.4s; }

.info-card:hover, .map-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.6);
  border-color: rgba(255, 255, 255, 0.2);
}

h2 {
  font-size: 24px;
  color: #000;
  margin: 0 0 1.5rem 0;
  font-weight: 800;
  letter-spacing: -0.01em;
}

.info-card p {
  color: #666;
  line-height: 1.7;
  margin: 0;
  font-weight: 500;
  font-size: 15px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.info-item:last-child {
  border-bottom: none;
}

.info-item strong {
  color: #666;
  font-weight: 700;
  font-size: 14px;
}

.info-item span {
  color: #000 !important;
  font-weight: 600;
  font-size: 14px;
}

.info-item p {
  color: #000 !important;
  margin: 0;
  font-weight: 600;
}

.status-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-status {
  padding: 1rem;
  border: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  background: #fff;
  color: #000;
}

.btn-status::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.btn-abierta::before {
  background: var(--warning, #ffcc00);
}

.btn-en-progreso::before {
  background: var(--info, #00ccff);
}

.btn-resuelta::before {
  background: var(--success, #00ff88);
}

.btn-status:hover::before {
  width: 300px;
  height: 300px;
}

.btn-status:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.resolver-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.resolver-section h3 {
  font-size: 18px;
  color: #fff;
  margin-bottom: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.01em;
}

.nota-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg, 12px);
  font-size: 14px;
  font-family: inherit;
  font-weight: 500;
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
  resize: vertical;
  margin-bottom: 1rem;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

.nota-textarea:focus {
  outline: none;
  border-color: var(--success, #00ff88);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
}

.btn-resolver {
  background: #fff;
  color: #000;
  width: 100%;
}

.btn-resolver::before {
  background: var(--success, #00ff88);
}

.btn-resolver:disabled {
  background: rgba(255, 255, 255, 0.2);
  cursor: not-allowed;
  opacity: 0.5;
  color: #666;
}

.btn-resolver:disabled::before {
  display: none;
}

.btn-en-progreso:disabled {
  background: rgba(255, 255, 255, 0.2);
  cursor: not-allowed;
  opacity: 0.5;
  color: #666;
}

.btn-en-progreso:disabled::before {
  display: none;
}

.warning-message {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 204, 0, 0.1);
  border-left: 4px solid var(--warning, #ffcc00);
  border-radius: var(--radius-lg, 12px);
  color: var(--warning, #ffcc00);
  font-size: 14px;
  font-weight: 600;
}

.resolucion-card {
  background: #fff;
  border-left: 4px solid var(--success, #00ff88);
  border: 2px solid var(--success, #00ff88);
}

.resolucion-card .info-item p {
  margin-top: 0.5rem;
  font-style: italic;
  color: #000 !important;
  font-weight: 700;
}

#detail-map {
  height: 300px;
  width: 100%;
  border-radius: var(--radius-lg, 12px);
  margin-bottom: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.btn-map-external {
  display: block;
  text-align: center;
  padding: 0.75rem 1.5rem;
  background: #fff;
  color: #000;
  text-decoration: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-map-external::before {
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

.btn-map-external:hover::before {
  width: 300px;
  height: 300px;
}

.btn-map-external:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.actions-section {
  display: flex;
  justify-content: space-between;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.5s backwards;
}

.btn-back {
  padding: 1rem 2rem;
  background: #fff;
  color: #000;
  text-decoration: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-back::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--success, #00ff88);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.btn-back:hover::before {
  width: 300px;
  height: 300px;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
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
    font-size: 36px;
  }

  .tipo-badge-detalle {
    font-size: 12px;
  }

  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .info-card,
  .map-card {
    padding: 1.5rem;
  }

  h2 {
    font-size: 20px;
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
    font-size: 28px;
  }

  .estado-badge {
    font-size: 11px;
    padding: 0.4rem 0.8rem;
  }

  .btn-status {
    font-size: 12px;
    padding: 0.85rem;
  }

  .nota-textarea {
    font-size: 14px;
  }

  .btn-back {
    width: 100%;
    text-align: center;
  }
}
</style>
