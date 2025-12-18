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
                <option value="accidente">Accidente</option>
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
              <div class="coordinates-info" v-if="formData.latitud && formData.longitud">
                <small>
                  📍 Coordenadas: {{ formData.latitud }}, {{ formData.longitud }}
                </small>
              </div>
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
                {{ isLoading ? 'Enviando...' : 'Reportar Incidencia' }}
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

const isLoading = ref(false)
const error = ref('')
const success = ref('')

let map = null
let marker = null

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
  
  marker.bindPopup(`📍 Ubicación seleccionada<br>Lat: ${lat}<br>Lng: ${lng}`).openPopup()
  
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
    const data = {
      tipo: formData.value.tipo,
      descripcion: formData.value.descripcion,
    }
    
    if (formData.value.direccion) {
      data.direccion = formData.value.direccion
    }
    
    if (formData.value.latitud && formData.value.longitud) {
      // Redondear a 6 decimales para cumplir con validación del backend
      data.latitud = parseFloat(parseFloat(formData.value.latitud).toFixed(6))
      data.longitud = parseFloat(parseFloat(formData.value.longitud).toFixed(6))
    }
    
    await incidenciaStore.create(data)
    
    success.value = 'Incidencia reportada exitosamente. Redirigiendo...'
    
    // Esperar un momento y recargar todas las incidencias antes de redirigir
    await new Promise(resolve => setTimeout(resolve, 500))
    await incidenciaStore.fetchAll()
    
    setTimeout(() => {
      router.push('/incidencias')
    }, 1500)
  } catch (err) {
    console.error('Error al reportar incidencia:', err)
    error.value = err.response?.data?.message || JSON.stringify(err.response?.data) || 'Error al reportar la incidencia'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.nueva-incidencia-content {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

textarea {
  resize: vertical;
}

.incidencia-map {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 2px solid #ddd;
}

.map-instructions {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  font-style: italic;
}

.coordinates-info {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: #f0f0f0;
  border-radius: 4px;
  text-align: center;
}

.coordinates-info small {
  color: #666;
  font-family: monospace;
}

.btn-secondary {
  width: 100%;
  padding: 0.75rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: opacity 0.3s;
}

.btn-secondary:hover {
  opacity: 0.9;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  background-color: #efe;
  color: #3c3;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-cancel:hover {
  opacity: 0.9;
}

.btn-submit {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-submit:hover {
  opacity: 0.9;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 768px) {
  .nueva-incidencia-content {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .form-container {
    padding: 1.25rem;
  }

  #map {
    height: 250px;
  }

  .location-buttons {
    flex-direction: column;
  }

  .btn-location {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .nueva-incidencia-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 1.25rem;
  }

  .form-container {
    padding: 1rem;
  }

  .form-group label {
    font-size: 0.9rem;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 0.9rem;
  }

  .btn-submit {
    width: 100%;
  }
}
</style>
