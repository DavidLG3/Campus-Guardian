<template>
  <div class="incidencias-view">
    <AppLayout>
      <div class="incidencias-content">
        <div class="header">
          <h1>Incidencias</h1>
          <router-link v-if="authStore.isCiudadano" to="/incidencias/nueva" class="btn-primary">
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
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const incidenciaStore = useIncidenciaStore()
const authStore = useAuthStore()

const filtroEstado = ref('')
const filtroTipo = ref('')
const isLoading = ref(false)
const error = ref('')

// Apply status/type filters over the store data.
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
  // Map backend status keys to readable labels.
  const estados = {
    'abierta': 'Abierta',
    'en_progreso': 'En Progreso',
    'resuelta': 'Resuelta'
  }
  return estados[estado] || estado
}

function formatTipo(tipo) {
  // Normalize incident type names for card badges.
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
  // Format timestamps for Spanish locale display.
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Load incidents when the view is mounted.
onMounted(async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    // Fetch the full list from the API via Pinia store.
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

.incidencias-content {
  padding: 3.5rem 2rem 2rem;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

h1 {
  font-size: 42px;
  color: #fff;
  margin: 0;
  font-weight: 900;
  letter-spacing: -0.02em;
}

.btn-primary {
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

.btn-primary::before {
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

.btn-primary:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

.filter-select {
  padding: 1rem 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg, 12px);
  font-size: 14px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

.filter-select option {
  background: #1a1a1a;
  color: #fff;
}

.filter-select:focus {
  outline: none;
  border-color: var(--success, #00ff88);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
}

.loading, .error, .empty {
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

.incidencias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.incidencia-card {
  background: #fff;
  border: 2px solid var(--success, #00ff88);
  border-radius: var(--radius-xl, 16px);
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.incidencia-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.05), rgba(0, 204, 255, 0.05));
  opacity: 0;
  transition: opacity var(--transition-base, 0.3s);
  pointer-events: none;
}

.incidencia-card:hover::after {
  opacity: 1;
}

.incidencia-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.4);
  border-color: var(--success, #00ff88);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1.5rem;
}

.card-header .header-left {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.codigo-principal {
  margin: 0;
  color: #000;
  font-size: 24px;
  font-weight: 900;
  letter-spacing: -0.01em;
}

.tipo-badge {
  display: inline-block;
  width: fit-content;
  padding: 0.5rem 1rem;
  background: #f0f0f0;
  color: #000;
  border-radius: var(--radius-full, 9999px);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid #e0e0e0;
}

.estado-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full, 9999px);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 2px solid;
}

.estado-badge.abierta {
  background: rgba(255, 204, 0, 0.2);
  color: #000;
  border-color: var(--warning, #ffcc00);
}

.estado-badge.en_progreso {
  background: rgba(0, 204, 255, 0.2);
  color: #000;
  border-color: var(--info, #00ccff);
}

.estado-badge.resuelta {
  background: rgba(0, 255, 136, 0.2);
  color: #000;
  border-color: var(--success, #00ff88);
}

.descripcion {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-weight: 500;
  font-size: 14px;
}

.card-info {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  gap: 0.75rem;
  font-size: 13px;
  color: #fff;
  align-items: center;
}

.info-item .label {
  color: #666;
  min-width: 120px;
  font-weight: 600;
}

.info-item span:not(.label) {
  color: #000;
  font-weight: 600;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.btn-view {
  color: #000;
  text-decoration: none;
  font-weight: 800;
  font-size: 14px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  transition: all var(--transition-fast, 0.15s);
  position: relative;
}

.btn-view::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--success, #00ff88);
  transition: width var(--transition-base, 0.3s);
}

.btn-view:hover {
  color: #000;
  transform: translateX(4px);
}

.btn-view:hover::after {
  width: 100%;
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
    font-size: 32px;
  }

  .header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
  }

  .btn-primary {
    width: 100%;
    text-align: center;
  }

  .filters {
    flex-direction: column;
  }

  .incidencias-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .codigo-principal {
    font-size: 20px;
  }

  .tipo-badge {
    font-size: 11px;
  }

  .descripcion {
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .incidencias-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 28px;
  }

  .incidencia-card {
    padding: 1.5rem;
  }

  .filter-select {
    font-size: 13px;
  }

  .codigo-principal {
    font-size: 18px;
  }

  .info-item {
    font-size: 12px;
    flex-direction: column;
    gap: 0.25rem;
    align-items: flex-start;
  }

  .info-item .label {
    min-width: auto;
  }
}
</style>
