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

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.alertas-content {
  padding: 2rem;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

.header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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

.subtitle {
  color: var(--text-secondary, #a0a0a0);
  font-size: 16px;
  font-weight: 600;
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
  border-color: var(--info, #00ccff);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 204, 255, 0.2);
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

.alertas-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.notificacion-card {
  background: #fff;
  border-radius: var(--radius-xl, 16px);
  padding: 2rem;
  border: 2px solid var(--success, #00ff88);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.notificacion-card.no-leida {
  border-left: 4px solid var(--info, #00ccff);
  background: #fff;
}

.notificacion-card:hover {
  transform: translateX(4px);
  border-color: var(--success, #00ff88);
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.4);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
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
  color: #000;
  font-size: 20px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.01em;
}

.badge-nueva {
  padding: 0.5rem 1rem;
  background: var(--info, #00ccff);
  color: #000;
  border-radius: var(--radius-full, 9999px);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  animation: pulse 2s ease-in-out infinite;
}

.mensaje {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  font-size: 15px;
  font-weight: 500;
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
  color: #000;
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
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-ver-incidencia {
  padding: 0.75rem 1.5rem;
  background: #fff;
  color: #000;
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
}

.btn-ver-incidencia::before {
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

.btn-ver-incidencia:hover::before {
  width: 300px;
  height: 300px;
}

.btn-ver-incidencia span {
  position: relative;
  z-index: 1;
}

.btn-ver-incidencia:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.btn-action {
  padding: 0.75rem 1.5rem;
  background: rgba(0, 255, 136, 0.2);
  color: var(--success, #00ff88);
  border: 2px solid var(--success, #00ff88);
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-action:hover {
  background: var(--success, #00ff88);
  color: #000;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

/* Responsive Design */
@media (max-width: 768px) {
  .alertas-content {
    padding: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .subtitle {
    font-size: 14px;
  }

  .filters {
    flex-direction: column;
  }

  .notificacion-card {
    padding: 1.5rem;
  }

  .card-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .btn-ver-incidencia,
  .btn-action {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .alertas-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 28px;
  }

  .filter-select {
    font-size: 13px;
  }

  .mensaje {
    font-size: 14px;
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
