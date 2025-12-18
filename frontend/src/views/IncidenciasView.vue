<template>
  <div class="incidencias-view">
    <AppLayout>
      <div class="incidencias-content">
        <div class="header">
          <h1>Incidencias</h1>
          <router-link to="/incidencias/nueva" class="btn-primary">
            ➕ Nueva Incidencia
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
            <option value="vandalismo">Vandalismo</option>
            <option value="accidente">Accidente</option>
            <option value="otro">Otro</option>
          </select>
        </div>
        
        <div v-if="isLoading" class="loading">Cargando incidencias...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-else-if="incidenciasFiltradas.length === 0" class="empty">
          No hay incidencias para mostrar
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
              
              <div v-if="incidencia.usuario_reporta" class="info-item">
                <span class="label">👤 Reportado por:</span>
                <span>{{ incidencia.usuario_reporta.nombre }}</span>
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
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()

const filtroEstado = ref('')
const filtroTipo = ref('')
const isLoading = ref(false)
const error = ref('')

const incidenciasFiltradas = computed(() => {
  let filtered = incidenciaStore.incidencias
  
  if (filtroEstado.value) {
    filtered = filtered.filter(i => i.estado === filtroEstado.value)
  }
  
  if (filtroTipo.value) {
    filtered = filtered.filter(i => i.tipo === filtroTipo.value)
  }
  
  return filtered
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
    console.error('Error al cargar las incidencias:', err)
    error.value = 'Error al cargar las incidencias. Por favor, recarga la página.'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.incidencias-content {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  text-transform: capitalize;
}

.estado-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
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

.descripcion {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.5;
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
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.btn-view:hover {
  color: #764ba2;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .incidencias-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .incidencias-content {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .filters {
    flex-direction: column;
  }

  .incidencias-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .codigo-principal {
    font-size: 1.25rem;
  }

  .tipo-badge {
    font-size: 0.75rem;
  }

  .descripcion {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .incidencias-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 1.25rem;
  }

  .btn-primary {
    width: 100%;
    text-align: center;
  }

  .filter-select {
    font-size: 0.9rem;
  }

  .codigo-principal {
    font-size: 1.1rem;
  }

  .info-item {
    font-size: 0.85rem;
    flex-direction: column;
    gap: 0.25rem;
  }

  .info-item .label {
    min-width: auto;
  }
}
</style>
