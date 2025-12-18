<template>
  <div class="alertas-view">
    <AppLayout>
      <div class="alertas-content">
        <div class="header">
          <h1>Notificaciones de Incidencias</h1>
          <p class="subtitle">Alertas automáticas sobre nuevas incidencias reportadas</p>
        </div>
        
        <div class="filters">
          <select v-model="filtroLeida" class="filter-select">
            <option value="">Todas</option>
            <option value="false">No leídas</option>
            <option value="true">Leídas</option>
          </select>
        </div>
        
        <div v-if="isLoading" class="loading">Cargando alertas...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-else-if="alertasFiltradas.length === 0" class="empty">
          No hay alertas para mostrar
        </div>
        
        <div v-else class="alertas-list">
          <div
            v-for="alerta in alertasFiltradas"
            :key="alerta.id"
            :class="['notificacion-card', { 'no-leida': !alerta.leida }]"
          >
          >
            <div class="card-header">
              <div class="header-left">
                <h3>{{ alerta.tipo }}</h3>
              </div>
              <div class="header-right">
                <span v-if="!alerta.leida" class="badge-nueva">Nueva</span>
              </div>
            </div>
            
            <p class="mensaje">{{ alerta.mensaje }}</p>
            
            <div class="card-info">
              <div class="info-item">
                <span class="label">📅 Fecha:</span>
                <span>{{ formatDate(alerta.fecha_creacion) }}</span>
              </div>
              
              <div v-if="alerta.ubicacion" class="info-item">
                <span class="label">📍 Ubicación:</span>
                <span>{{ alerta.ubicacion }}</span>
              </div>
            </div>
            
            <div class="card-actions">
              <button
                @click="verIncidencia(alerta)"
                class="btn-ver-incidencia"
              >
                📋 Ver Incidencia
              </button>
              <button
                v-if="!alerta.leida"
                @click="marcarComoLeida(alerta.id)"
                class="btn-action"
              >
                ✓ Marcar como leída
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAlertaStore } from '@/stores/alerta'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const router = useRouter()
const alertaStore = useAlertaStore()
const authStore = useAuthStore()

const filtroLeida = ref('')
const isLoading = ref(false)
const error = ref('')

const alertasFiltradas = computed(() => {
  let filtered = alertaStore.alertas
  
  if (filtroLeida.value !== '') {
    const leida = filtroLeida.value === 'true'
    filtered = filtered.filter(a => a.leida === leida)
  }
  
  return filtered.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
})

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

function verIncidencia(alerta) {
  if (alerta.incidencia) {
    router.push(`/incidencias/${alerta.incidencia}`)
  }
}

async function marcarComoLeida(id) {
  try {
    await alertaStore.markAsRead(id)
    // Recargar todas las alertas para actualizar el contador
    await alertaStore.fetchAll()
  } catch (err) {
    console.error('Error al marcar alerta como leída:', err)
  }
}

onMounted(async () => {
  isLoading.value = true
  error.value = ''
  
  try {
    await alertaStore.fetchAll()
  } catch (err) {
    console.error('Error al cargar las alertas:', err)
    error.value = 'Error al cargar las alertas. Por favor, recarga la página.'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.alertas-content {
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

.alertas-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.notificacion-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #667eea;
}

.notificacion-card.no-leida {
  background-color: #f8f9fa;
  border-left-color: #667eea;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  gap: 0.5rem;
}

h3 {
  margin: 0;
  color: #333;
  font-size: 1.25rem;
  text-transform: capitalize;
}

.badge-nueva {
  padding: 0.25rem 0.75rem;
  background-color: #667eea;
  color: white;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.mensaje {
  color: #333;
  margin-bottom: 1rem;
  line-height: 1.6;
  font-size: 1.05rem;
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

.info-item span {
  color: #333;
}

.card-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-ver-incidencia {
  padding: 0.5rem 1rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-ver-incidencia:hover {
  opacity: 0.9;
}

.btn-action {
  padding: 0.5rem 1rem;
  background-color: #198754;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-action:hover {
  opacity: 0.9;
}

/* Responsive Design */
@media (max-width: 768px) {
  .alertas-content {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.9rem;
  }

  .filters {
    flex-direction: column;
  }

  .notificacion-card {
    padding: 1rem;
  }

  .card-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-ver-incidencia,
  .btn-action {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .alertas-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 1.25rem;
  }

  .filter-select {
    font-size: 0.9rem;
  }

  .mensaje {
    font-size: 0.95rem;
  }

  .info-item {
    font-size: 0.85rem;
  }
}
</style>
