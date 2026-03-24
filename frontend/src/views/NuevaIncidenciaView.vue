<template>
  <div class="nueva-incidencia-view">
    <AppLayout>
      <div class="nueva-incidencia-content">
        <h1>Reportar Nueva Incidencia</h1>
        
        <div class="form-container">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="tipo">Tipo de Incidencia *</label>
              <select id="tipo" v-model="formData.tipo" required>
                <option value="">Selecciona un tipo</option>
                <option value="robo">Robo</option>
                <option value="vandalismo">Vandalismo</option>
                <option value="incendio">Incendio</option>
                <option value="situacion_incomoda">Situación Incómoda</option>
                <option value="estafa">Estafa</option>
                <option value="accidente">Accidente</option>
                <option value="incendio">Incendio</option>
                <option value="vandalismo">Vandalismo</option>
                <option value="situacion_incomoda">Situación Incómoda</option>
                <option value="estafa">Estafa</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="descripcion">Descripción *</label>
              <textarea
                id="descripcion"
                v-model="formData.descripcion"
                required
                rows="4"
                placeholder="Describe la incidencia con el mayor detalle posible..."
              ></textarea>
            </div>
            
            <div class="form-group">
              <label>Ubicación en el Mapa *</label>
              <p class="map-instructions">
                Haz clic en el mapa para seleccionar la ubicación de la incidencia
              </p>
              <div id="incidencia-map" class="incidencia-map"></div>
              <button 
                type="button" 
                @click="getCurrentLocation" 
                class="btn-secondary"
                :disabled="isLoading"
              >
                📍 Usar Mi Ubicación
              </button>
            </div>
            
            <div class="form-group">
              <label for="direccion">Dirección (opcional)</label>
              <input
                id="direccion"
                v-model="formData.direccion"
                type="text"
                placeholder="Escribe la dirección si lo deseas..."
              />
            </div>
            
            <!-- Sección de archivos multimedia -->
            <div class="form-group">
              <label>Fotos y Videos (opcional)</label>
              <p class="field-description">
                Puedes adjuntar fotos o videos relacionados con la incidencia
              </p>
              <MediaCapture ref="mediaCaptureRef" @files-selected="handleFilesSelected" />
            </div>
            
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
            
            <div v-if="success" class="success-message">
              {{ success }}
            </div>
            
            <div class="form-actions">
              <router-link to="/incidencias" class="btn-cancel">
                Cancelar
              </router-link>
              <button type="submit" :disabled="isLoading" class="btn-submit">
                <span>{{ isLoading ? 'Enviando...' : 'Reportar Incidencia' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useIncidenciaStore } from '@/stores/incidencia'
import AppLayout from '@/layouts/AppLayout.vue'
import MediaCapture from '@/components/MediaCapture.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const router = useRouter()
const incidenciaStore = useIncidenciaStore()

const formData = ref({
  tipo: '',
  descripcion: '',
  direccion: '',
  latitud: null,
  longitud: null
})

const mediaCaptureRef = ref(null)
const selectedFiles = ref([])

const isLoading = ref(false)
const error = ref('')
const success = ref('')

let map = null
let marker = null

const handleFilesSelected = (files) => {
  selectedFiles.value = files
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})

function initMap() {
  // Coordenadas por defecto (Campus de Cantoblanco, UAM)
  const defaultLat = 40.5472
  const defaultLng = -3.6894
  
  map = L.map('incidencia-map').setView([defaultLat, defaultLng], 15)
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)
  
  // Evento de click en el mapa
  map.on('click', (e) => {
    const lat = parseFloat(e.latlng.lat.toFixed(6))
    const lng = parseFloat(e.latlng.lng.toFixed(6))
    
    formData.value.latitud = lat
    formData.value.longitud = lng
    
    updateMarker(lat, lng)
  })
}

function updateMarker(lat, lng) {
  // Remover marcador anterior si existe
  if (marker) {
    map.removeLayer(marker)
  }
  
  // Crear nuevo marcador
  marker = L.marker([lat, lng], {
    icon: L.icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    })
  }).addTo(map)
  
  // No mostrar popup, solo el marcador
  
  // Centrar mapa en el marcador
  map.setView([lat, lng], 15)
}

function getCurrentLocation() {
  if ('geolocation' in navigator) {
    isLoading.value = true
    isLoading.value = true
    navigator.geolocation.getCurrentPosition(
      (position) => {
        // Redondear a 6 decimales para que coincida con el backend
        const lat = parseFloat(position.coords.latitude.toFixed(6))
        const lng = parseFloat(position.coords.longitude.toFixed(6))
        
        formData.value.latitud = lat
        formData.value.longitud = lng
        
        updateMarker(lat, lng)
        
        success.value = 'Ubicación obtenida correctamente'
        isLoading.value = false
        setTimeout(() => { success.value = '' }, 3000)
      },
      (err) => {
        isLoading.value = false
        error.value = 'No se pudo obtener la ubicación: ' + err.message
      }
    )
  } else {
    error.value = 'Tu navegador no soporta geolocalización'
  }
}

async function handleSubmit() {
  error.value = ''
  success.value = ''
  isLoading.value = true
  
  try {
    // Crear FormData para enviar archivos
    const formDataToSend = new FormData()
    
    formDataToSend.append('tipo', formData.value.tipo)
    formDataToSend.append('descripcion', formData.value.descripcion)
    
    if (formData.value.direccion) {
      formDataToSend.append('direccion', formData.value.direccion)
    }
    
    if (formData.value.latitud && formData.value.longitud) {
      // Redondear a 6 decimales para cumplir con validación del backend
      formDataToSend.append('latitud', parseFloat(parseFloat(formData.value.latitud).toFixed(6)))
      formDataToSend.append('longitud', parseFloat(parseFloat(formData.value.longitud).toFixed(6)))
    }
    
    // Agregar archivos si existen
    if (selectedFiles.value && selectedFiles.value.length > 0) {
      console.log('📎 Archivos a enviar:', selectedFiles.value.length)
      selectedFiles.value.forEach((file, index) => {
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2)
        console.log(`  ${index + 1}. ${file.name} (${file.type}) - ${sizeMB}MB`)
        formDataToSend.append('archivos', file)
      })
    }
    
    console.log('📤 Enviando incidencia...')
    await incidenciaStore.create(formDataToSend)
    
    success.value = 'Incidencia reportada exitosamente. Redirigiendo...'
    
    // Limpiar archivos
    if (mediaCaptureRef.value) {
      mediaCaptureRef.value.clearFiles()
    }
    selectedFiles.value = []
    
    // Esperar un momento y recargar todas las incidencias antes de redirigir
    await new Promise(resolve => setTimeout(resolve, 500))
    await incidenciaStore.fetchAll()
    
    setTimeout(() => {
      router.push('/incidencias')
    }, 1500)
  } catch (err) {
    console.error('❌ Error al reportar incidencia:', err)
    console.error('📋 Respuesta del servidor:', err.response?.data)
    console.error('🔢 Status code:', err.response?.status)
    console.error('📄 Headers:', err.response?.headers)
    
    // Intentar extraer mensaje de error útil
    let errorMsg = 'Error al reportar la incidencia'
    
    if (err.response?.data) {
      if (typeof err.response.data === 'string') {
        errorMsg = err.response.data.substring(0, 200) // Limitar texto
      } else if (err.response.data.error) {
        errorMsg = err.response.data.error
      } else if (err.response.data.detail) {
        errorMsg = err.response.data.detail
      } else {
        errorMsg = JSON.stringify(err.response.data).substring(0, 200)
      }
    }
    
    error.value = errorMsg
  } finally {
    isLoading.value = false
  }
}
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

.nueva-incidencia-content {
  padding: 2.5rem 2rem 2rem;
  max-width: 800px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

h1 {
  font-size: 42px;
  margin-bottom: 3rem;
  color: #fff;
  font-weight: 900;
  letter-spacing: -0.02em;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.form-container {
  background: #fff;
  padding: 3rem;
  border-radius: var(--radius-2xl, 20px);
  border: 2px solid var(--success, #00ff88);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

.form-group {
  margin-bottom: 2rem;
}

.form-group:last-of-type {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.75rem;
  color: #000;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

input,
textarea,
select {
  width: 100%;
  padding: 1rem 1.25rem;
  background: #f8f8f8;
  border: 2px solid #e0e0e0;
  border-radius: var(--radius-lg, 12px);
  font-size: 16px;
  color: #000;
  font-weight: 600;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

input::placeholder,
textarea::placeholder {
  color: rgba(0, 0, 0, 0.4);
}

select option {
  background: #fff;
  color: #000;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: var(--success, #00ff88);
  background: #fff;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 255, 136, 0.2);
}

textarea {
  resize: vertical;
  line-height: 1.6;
}

.incidencia-map {
  width: 100%;
  height: 400px;
  border-radius: var(--radius-lg, 12px);
  margin-bottom: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.map-instructions {
  color: var(--text-secondary, #a0a0a0);
  font-size: 14px;
  margin-bottom: 1rem;
  font-style: italic;
  font-weight: 500;
}

.field-description {
  color: var(--text-secondary, #a0a0a0);
  font-size: 13px;
  margin: 8px 0 12px 0;
  font-style: italic;
}

.btn-secondary {
  width: 100%;
  padding: 1rem 1.5rem;
  background: #f0f0f0;
  color: #000;
  border: 2px solid #d0d0d0;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-secondary:hover {
  background: #00ff88;
  border-color: #00ff88;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

.btn-secondary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background: linear-gradient(135deg, rgba(255, 68, 68, 0.2) 0%, rgba(255, 68, 68, 0.1) 100%);
  color: var(--error, #ff4444);
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg, 12px);
  border: 2px solid rgba(255, 68, 68, 0.3);
  margin-bottom: 1.5rem;
  font-weight: 700;
  font-size: 14px;
}

.success-message {
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%);
  color: var(--success, #00ff88);
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg, 12px);
  border: 2px solid rgba(0, 255, 136, 0.3);
  margin-bottom: 1.5rem;
  font-weight: 700;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-cancel {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.15);
}

.btn-submit {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  color: #000;
  border: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 900;
  font-size: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
}

.btn-submit span {
  position: relative;
  z-index: 1;
  font-weight: 900;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.6);
  background: linear-gradient(135deg, #00ffaa 0%, #00dd88 100%);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-submit:disabled:hover {
  transform: none;
  box-shadow: none;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
}

/* Responsive Design */
@media (max-width: 768px) {
  .nueva-incidencia-content {
    padding: 1.5rem 1rem 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .form-container {
    padding: 2rem;
  }

  .incidencia-map {
    height: 300px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .nueva-incidencia-content {
    padding: 1.25rem 0.75rem 0.75rem;
  }

  h1 {
    font-size: 28px;
  }

  .form-container {
    padding: 1.5rem;
  }

  .incidencia-map {
    height: 250px;
  }

  .form-actions {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
    text-align: center;
  }
}
</style>
