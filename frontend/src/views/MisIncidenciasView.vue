<template>
  <div class="mis-incidencias-view">
    <AppLayout>
      <div class="mis-incidencias-content">
        <div class="header">
          <h1>Mis Incidencias</h1>
          <router-link to="/incidencias/nueva" class="btn-primary">
            + Nueva Incidencia
          </router-link>
        </div>
        
        <div class="filters">
          <select v-model="filtroEstado" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="abierta">Abiertas</option>
            <option value="en_progreso">En Progreso</option>
            <option value="resuelta">Resueltas</option>
          </select>
          
          <select v-model="filtroTipo" class="filter-select">
            <option value="">Todos los tipos</option>
            <option value="robo">Robo</option>
            <option value="accidente">Accidente</option>
            <option value="incendio">Incendio</option>
            <option value="vandalismo">Vandalismo</option>
            <option value="situacion_incomoda">Situación Incómoda</option>
            <option value="estafa">Estafa</option>
            <option value="otro">Otro</option>
          </select>
        </div>
        
        <div v-if="isLoading" class="loading">Cargando mis incidencias...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-else-if="incidenciasFiltradas.length === 0" class="empty">
          <p>No tienes incidencias reportadas</p>
          <router-link to="/incidencias/nueva" class="btn-primary">
            Reportar Primera Incidencia
          </router-link>
        </div>
        
        <div v-else class="incidencias-grid">
          <div
            v-for="incidencia in incidenciasFiltradas"
            :key="incidencia.id"
            class="incidencia-card"
          >
            <div class="card-header">
              <div class="header-left">
                <h2 class="codigo-principal">{{ incidencia.codigo_unico }}</h2>
                <span class="tipo-badge">{{ formatTipo(incidencia.tipo) }}</span>
              </div>
              <span :class="['estado-badge', incidencia.estado]">
                {{ formatEstado(incidencia.estado) }}
              </span>
            </div>
            
            <p class="descripcion">{{ incidencia.descripcion || 'Sin descripción' }}</p>
            
            <div class="card-info">
              <div class="info-item">
                <span class="label">📅 Fecha:</span>
                <span>{{ formatDate(incidencia.fecha_creacion) }}</span>
              </div>
              
              <div v-if="incidencia.direccion" class="info-item">
                <span class="label">📍 Dirección:</span>
                <span>{{ incidencia.direccion }}</span>
              </div>
            </div>
            
            <div class="card-actions">
              <router-link :to="`/incidencias/${incidencia.id}`" class="btn-view">
                Ver Detalles →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useIncidenciaStore } from '@/stores/incidencia'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()
const authStore = useAuthStore()

const filtroTipo = ref('')
const filtroEstado = ref('')
const isLoading = ref(false)
const error = ref('')

const incidenciasFiltradas = computed(() => {
  let filtered = incidenciaStore.incidencias.filter(inc => {
    // Solo mostrar incidencias del usuario actual
    return inc.usuario === authStore.user?.id
  })
  
  if (filtroTipo.value) {
    filtered = filtered.filter(i => i.tipo === filtroTipo.value)
  }
  
  if (filtroEstado.value) {
    filtered = filtered.filter(i => i.estado === filtroEstado.value)
  }
  
  return filtered.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
})

function formatEstado(estado) {
  const estados = {
    'abierta': 'Abierta',
    'en_progreso': 'En Progreso',
    'resuelta': 'Resuelta',
    'pendiente': 'Pendiente'
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
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    await incidenciaStore.fetchAll()
  } catch (err) {
    console.error('Error al cargar mis incidencias:', err)
    error.value = 'Error al cargar las incidencias. Por favor, recarga la página.'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.mis-incidencias-content {
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin: 0;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background-color: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
}

.loading, .error, .empty {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.error {
  color: #dc3545;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty p {
  font-size: 1.1rem;
  color: #666;
}

.incidencias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.incidencia-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.incidencia-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.card-header .header-left {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.codigo-principal {
  margin: 0;
  color: #1976d2;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.tipo-badge {
  display: inline-block;
  width: fit-content;
  padding: 0.25rem 0.75rem;
  background-color: #f5f5f5;
  color: #666;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.estado-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.estado-badge.abierta, .estado-badge.pendiente {
  background-color: #cfe2ff;
  color: #084298;
}

.estado-badge.en_progreso {
  background-color: #fff3cd;
  color: #856404;
}

.estado-badge.resuelta {
  background-color: #d1e7dd;
  color: #0f5132;
}

.descripcion {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-info {
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #333;
}

.info-item .label {
  color: #999;
  min-width: 120px;
}

.info-item span:not(.label) {
  color: #333 !important;
  font-weight: 400;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-view {
  padding: 0.5rem 1rem;
  background-color: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-view:hover {
  opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 768px) {
  .mis-incidencias-content {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .incidencias-grid {
    grid-template-columns: 1fr;
  }

  .codigo-principal {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .btn-primary {
    width: 100%;
    text-align: center;
  }

  .codigo-principal {
    font-size: 1.1rem;
  }
}
</style>
