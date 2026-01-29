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
              
              <!-- Sección de archivos adjuntos -->
              <div v-if="incidencia.archivos && incidencia.archivos.length > 0" class="info-card">
                <h2>Archivos Adjuntos ({{ incidencia.archivos.length }})</h2>
                <div class="archivos-grid">
                  <div v-for="archivo in incidencia.archivos" :key="archivo.id" class="archivo-item">
                    <div v-if="archivo.tipo === 'imagen'" class="archivo-preview">
                      <img :src="archivo.archivo_url" :alt="archivo.descripcion || 'Imagen'" @click="openImageModal(archivo.archivo_url)" />
                    </div>
                    <div v-else-if="archivo.tipo === 'video'" class="archivo-preview">
                      <video :src="archivo.archivo_url" controls></video>
                    </div>
                    <div class="archivo-info">
                      <span class="archivo-fecha">{{ formatDate(archivo.fecha_subida) }}</span>
                    </div>
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
          
          <!-- Sección de Comentarios -->
          <div class="comentarios-section">
            <div class="comentarios-header">
              <h2>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                Comentarios ({{ comentarios.length }})
              </h2>
              <p class="comentarios-subtitle">Comparte información adicional sobre esta incidencia</p>
            </div>

            <!-- Formulario para nuevo comentario -->
            <div class="nuevo-comentario">
              <div class="avatar-input-group">
                <div class="user-avatar">
                  <img 
                    v-if="authStore.user?.foto_perfil_url" 
                    :src="authStore.user.foto_perfil_url" 
                    alt="Avatar"
                  />
                  <div v-else class="avatar-placeholder">
                    {{ (authStore.user?.nombre || authStore.user?.username || '?').charAt(0).toUpperCase() }}
                  </div>
                </div>
                <textarea
                  v-model="nuevoComentario"
                  placeholder="Escribe un comentario..."
                  rows="3"
                  @keydown.ctrl.enter="submitComentario"
                ></textarea>
              </div>
              <div class="comentario-actions">
                <span class="hint">Ctrl + Enter para enviar</span>
                <button 
                  @click="submitComentario" 
                  :disabled="!nuevoComentario.trim() || isSubmittingComentario"
                  class="btn-submit-comentario"
                >
                  <svg v-if="!isSubmittingComentario" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                  <span v-if="isSubmittingComentario">Enviando...</span>
                  <span v-else>Enviar</span>
                </button>
              </div>
            </div>

            <!-- Lista de comentarios -->
            <div v-if="comentarios.length > 0" class="comentarios-list">
              <div 
                v-for="comentario in comentarios" 
                :key="comentario.id" 
                class="comentario-item"
              >
                <div class="comentario-avatar">
                  <img 
                    v-if="comentario.usuario_info.foto_perfil_url" 
                    :src="comentario.usuario_info.foto_perfil_url" 
                    alt="Avatar"
                  />
                  <div v-else class="avatar-placeholder">
                    {{ comentario.usuario_info.nombre.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <div class="comentario-content">
                  <div class="comentario-header-info">
                    <span class="comentario-autor">
                      {{ comentario.usuario_info.nombre }}
                    </span>
                    <span class="comentario-badge" v-if="comentario.usuario_info.tipo !== 'normal'" :class="comentario.usuario_info.tipo">
                      {{ formatTipoUsuario(comentario.usuario_info.tipo) }}
                    </span>
                    <span class="comentario-fecha">
                      {{ formatDateRelative(comentario.fecha_creacion) }}
                    </span>
                  </div>
                  <p class="comentario-texto">{{ comentario.contenido }}</p>
                  <div v-if="canDeleteComentario(comentario)" class="comentario-actions-btn">
                    <button @click="confirmDeleteComentario(comentario.id)" class="btn-delete-comentario">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="comentarios-empty">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
              <p>Aún no hay comentarios</p>
              <p class="small">Sé el primero en comentar</p>
            </div>
          </div>
          
          <div class="actions-section">
            <router-link to="/incidencias" class="btn-back">
              ← Volver a Incidencias
            </router-link>
          </div>
        </div>
        
        <!-- Modal para ver imágenes en grande -->
        <div v-if="selectedImage" class="image-modal" @click="selectedImage = null">
          <div class="modal-content" @click.stop>
            <button class="modal-close" @click="selectedImage = null">✕</button>
            <img :src="selectedImage" alt="Vista ampliada" />
          </div>
        </div>

        <!-- Modal de confirmación de eliminación -->
        <div v-if="showDeleteModal" class="delete-modal-overlay" @click="cancelDelete">
          <div class="delete-modal" @click.stop>
            <div class="delete-modal-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ff4336" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
            <h3>Eliminar Comentario</h3>
            <p>¿Estás seguro de que quieres eliminar este comentario?</p>
            <p class="warning-text">Esta acción no se puede deshacer.</p>
            <div class="delete-modal-actions">
              <button @click="cancelDelete" class="btn-cancel">
                Cancelar
              </button>
              <button @click="deleteComentario" class="btn-confirm-delete">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
                Eliminar
              </button>
            </div>
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
import comentarioService from '@/services/comentarioService'
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
const selectedImage = ref(null)
const comentarios = ref([])
const nuevoComentario = ref('')
const isSubmittingComentario = ref(false)
const showDeleteModal = ref(false)
const comentarioToDelete = ref(null)
let map = null

const openImageModal = (url) => {
  selectedImage.value = url
}

const canChangeStatus = computed(() => 
  authStore.isOperador // Solo el personal de seguridad puede cambiar estados
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
  }
}

onMounted(async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    const id = route.params.id
    const data = await incidenciaStore.fetchById(id)
    incidencia.value = data
    
    // Cargar comentarios
    await loadComentarios()
    
    // Inicializar mapa después de cargar los datos
    setTimeout(initMap, 100)
  } catch (err) {
    console.error('Error al cargar la incidencia:', err)
    error.value = 'Error al cargar la incidencia. Puede que no exista o no tengas permisos.'
  } finally {
    isLoading.value = false
  }
})

// Funciones para comentarios
const loadComentarios = async () => {
  try {
    console.log('Cargando comentarios para incidencia:', route.params.id)
    const response = await comentarioService.getComentariosByIncidencia(route.params.id)
    console.log('Comentarios recibidos:', response.data)
    // El endpoint devuelve formato paginado con results
    comentarios.value = response.data.results || response.data
  } catch (err) {
    console.error('Error cargando comentarios:', err)
  }
}

const submitComentario = async () => {
  if (!nuevoComentario.value.trim() || isSubmittingComentario.value) return
  
  isSubmittingComentario.value = true
  const contenidoTemp = nuevoComentario.value.trim()
  
  try {
    console.log('Enviando comentario:', {
      incidencia: route.params.id,
      contenido: contenidoTemp
    })
    
    const response = await comentarioService.createComentario({
      incidencia: route.params.id,
      contenido: contenidoTemp
    })
    
    console.log('Comentario creado:', response.data)
    
    // Limpiar el textarea solo después de éxito
    nuevoComentario.value = ''
    
    // Recargar comentarios
    await loadComentarios()
    
  } catch (err) {
    console.error('Error completo:', err)
    console.error('Response:', err.response)
    alert('Error al crear el comentario: ' + (err.response?.data?.detail || err.message))
  } finally {
    // Asegurar que siempre se desbloquee el botón
    isSubmittingComentario.value = false
  }
}

const canDeleteComentario = (comentario) => {
  return authStore.user?.id === comentario.usuario_info.id || authStore.isAdmin
}

const confirmDeleteComentario = (comentarioId) => {
  comentarioToDelete.value = comentarioId
  showDeleteModal.value = true
}

const cancelDelete = () => {
  showDeleteModal.value = false
  comentarioToDelete.value = null
}

const deleteComentario = async () => {
  if (!comentarioToDelete.value) return
  
  try {
    await comentarioService.deleteComentario(comentarioToDelete.value)
    await loadComentarios()
    showDeleteModal.value = false
    comentarioToDelete.value = null
  } catch (err) {
    console.error('Error eliminando comentario:', err)
    alert('Error al eliminar el comentario')
  }
}

const formatTipoUsuario = (tipo) => {
  const tipos = {
    'administrador': 'Admin',
    'operador': 'Operador',
    'ciudadano': 'Ciudadano'
  }
  return tipos[tipo] || tipo
}

const formatDateRelative = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (seconds < 60) return 'Ahora'
  if (minutes < 60) return `Hace ${minutes} min`
  if (hours < 24) return `Hace ${hours}h`
  if (days === 1) return 'Ayer'
  if (days < 7) return `Hace ${days} días`
  
  return formatDate(dateString)
}

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

.btn-resolver::before {
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
  border: 2px solid #d0d0d0;
  border-radius: var(--radius-lg, 12px);
  font-size: 14px;
  font-family: inherit;
  font-weight: 500;
  color: #000;
  background: #f8f8f8;
  resize: vertical;
  margin-bottom: 1rem;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

.nota-textarea:focus {
  outline: none;
  border-color: var(--success, #00ff88);
  background: #fff;
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

/* Archivos adjuntos */
.archivos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.archivo-item {
  background: #f5f5f5;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.archivo-item:hover {
  border-color: #00ff88;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.2);
}

.archivo-preview {
  width: 100%;
  height: 200px;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.archivo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.archivo-preview img:hover {
  transform: scale(1.05);
}

.archivo-preview video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.archivo-info {
  padding: 12px;
  background: white;
}

.archivo-fecha {
  font-size: 12px;
  color: #666;
}

/* Modal de imagen */
.image-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  cursor: pointer;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  cursor: default;
}

.modal-content img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}

.modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  width: 36px;
  height: 36px;
  background: #00ff88;
  border: none;
  border-radius: 50%;
  color: #000;
  font-size: 24px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: #00dd77;
  transform: rotate(90deg);
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

/* Estilos para Comentarios */
.comentarios-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem 0;
  border: 1px solid rgba(0, 255, 136, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.comentarios-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(0, 255, 136, 0.2);
}

.comentarios-header h2 {
  color: #00ff88;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.comentarios-header h2 svg {
  stroke: #00ff88;
}

.comentarios-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.nuevo-comentario {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid rgba(0, 255, 136, 0.15);
}

.avatar-input-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.user-avatar {
  flex-shrink: 0;
}

.user-avatar img,
.avatar-placeholder {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #00ff88;
}

.avatar-placeholder {
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0a0e27;
  font-weight: 700;
  font-size: 18px;
}

.avatar-input-group textarea {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 10px;
  padding: 1rem;
  color: white;
  font-size: 15px;
  font-family: inherit;
  resize: vertical;
  min-height: 80px;
  transition: all 0.3s ease;
}

.avatar-input-group textarea:focus {
  outline: none;
  border-color: #00ff88;
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1);
}

.avatar-input-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.comentario-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comentario-actions .hint {
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.btn-submit-comentario {
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  color: #0a0e27;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
}

.btn-submit-comentario:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4);
}

.btn-submit-comentario:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-submit-comentario svg {
  stroke: #0a0e27;
}

.comentarios-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comentario-item {
  display: flex;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  animation: slideUp 0.4s ease;
}

.comentario-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(0, 255, 136, 0.2);
  transform: translateX(5px);
}

.comentario-avatar img,
.comentario-avatar .avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(0, 255, 136, 0.5);
}

.comentario-avatar .avatar-placeholder {
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.3) 0%, rgba(0, 204, 111, 0.3) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #00ff88;
  font-weight: 600;
  font-size: 16px;
}

.comentario-content {
  flex: 1;
}

.comentario-header-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.comentario-autor {
  color: #00ff88;
  font-weight: 600;
  font-size: 15px;
}

.comentario-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.comentario-badge.administrador {
  background: rgba(255, 67, 54, 0.2);
  color: #ff4336;
  border: 1px solid rgba(255, 67, 54, 0.3);
}

.comentario-badge.operador {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border: 1px solid rgba(33, 150, 243, 0.3);
}

.comentario-badge.ciudadano {
  background: rgba(156, 39, 176, 0.2);
  color: #9c27b0;
  border: 1px solid rgba(156, 39, 176, 0.3);
}

.comentario-fecha {
  color: rgba(255, 255, 255, 0.4);
  font-size: 13px;
}

.comentario-texto {
  color: rgba(255, 255, 255, 0.85);
  font-size: 15px;
  line-height: 1.6;
  margin: 0 0 0.75rem 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.comentario-actions-btn {
  display: flex;
  gap: 0.5rem;
}

.btn-delete-comentario {
  background: transparent;
  color: rgba(255, 67, 54, 0.8);
  border: 1px solid rgba(255, 67, 54, 0.3);
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.3s ease;
}

.btn-delete-comentario:hover {
  background: rgba(255, 67, 54, 0.1);
  color: #ff4336;
  border-color: #ff4336;
}

.btn-delete-comentario svg {
  stroke: currentColor;
}

.comentarios-empty {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.4);
}

.comentarios-empty svg {
  margin-bottom: 1rem;
  stroke: rgba(0, 255, 136, 0.3);
}

.comentarios-empty p {
  margin: 0.5rem 0;
  font-size: 16px;
}

.comentarios-empty p.small {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.3);
}

@media (max-width: 768px) {
  .comentarios-section {
    padding: 1.25rem;
    margin: 1.5rem 0;
  }

  .comentarios-header h2 {
    font-size: 20px;
  }

  .nuevo-comentario {
    padding: 1rem;
  }

  .avatar-input-group {
    flex-direction: column;
  }

  .comentario-item {
    padding: 1rem;
  }

  .comentario-actions {
    flex-direction: column;
    gap: 0.75rem;
    align-items: stretch;
  }

  .btn-submit-comentario {
    width: 100%;
    justify-content: center;
  }
}

/* Modal de confirmación de eliminación */
.delete-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  animation: fadeIn 0.2s ease;
  backdrop-filter: blur(4px);
}

.delete-modal {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 16px;
  padding: 2rem;
  max-width: 420px;
  width: 90%;
  border: 2px solid rgba(255, 67, 54, 0.3);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.3s ease;
  text-align: center;
}

.delete-modal-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.delete-modal h3 {
  color: #ff4336;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 1rem;
}

.delete-modal p {
  color: rgba(255, 255, 255, 0.85);
  font-size: 15px;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.delete-modal .warning-text {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  font-style: italic;
  margin-bottom: 2rem;
}

.delete-modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.delete-modal-actions button {
  flex: 1;
  padding: 0.85rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-confirm-delete {
  background: linear-gradient(135deg, #ff4336 0%, #d32f2f 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(255, 67, 54, 0.3);
}

.btn-confirm-delete:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 67, 54, 0.5);
}

.btn-confirm-delete svg {
  stroke: white;
}

@media (max-width: 480px) {
  .delete-modal {
    padding: 1.5rem;
  }

  .delete-modal-actions {
    flex-direction: column;
  }

  .delete-modal-actions button {
    width: 100%;
  }
}
</style>

