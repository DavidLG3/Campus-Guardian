<template>
  <div class="notificaciones-view">
    <AppLayout>
      <div class="notificaciones-content">
        <h1>🔔 Mis Notificaciones</h1>
        
        <div v-if="isLoading" class="loading">Cargando notificaciones...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-show="!isLoading && !error && notificaciones.length === 0" class="empty">
          <p>No tienes notificaciones</p>
        </div>
        
        <div v-show="!isLoading && !error && notificaciones.length > 0" class="notificaciones-list">
          <div 
            v-for="notificacion in notificaciones" 
            :key="notificacion.id"
            :class="['notificacion-card', { 'no-leida': !notificacion.leida }]"
          >
            <div class="notif-icon">
              <span v-if="notificacion.tipo === 'en_progreso'">🚀</span>
              <span v-else-if="notificacion.tipo === 'resuelta'">✅</span>
            </div>
            <div class="notif-content">
              <div class="notif-header">
                <span class="notif-codigo">{{ notificacion.incidencia_codigo || 'N/A' }}</span>
                <span class="notif-fecha">{{ formatDate(notificacion.fecha_creacion) }}</span>
              </div>
              <p class="notif-mensaje">{{ notificacion.mensaje }}</p>
              <button 
                v-if="!notificacion.leida"
                @click="marcarComoLeida(notificacion.id)"
                class="btn-marcar-leida"
              >
                Marcar como leída
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useNotificacionStore } from '@/stores/notificacion'
import AppLayout from '@/layouts/AppLayout.vue'

const notificacionStore = useNotificacionStore()

// Use the store's refs directly to avoid creating new arrays
const notificaciones = computed(() => notificacionStore.notificaciones)
const isLoading = computed(() => notificacionStore.isLoading)
const error = computed(() => notificacionStore.error)

function formatDate(dateString) {
  // Keep date rendering consistent across all notification cards.
  const date = new Date(dateString)
  return date.toLocaleString('es-ES', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function marcarComoLeida(id) {
  try {
    // Persist read state in backend and update store state.
    await notificacionStore.markAsRead(id)
  } catch (err) {
    console.error('Error al marcar notificación como leída:', err)
  }
}

onMounted(() => {
  // Load notifications once when the view is mounted.
  notificacionStore.fetchAll()
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

.notificaciones-content {
  padding: 3.5rem 2rem 2rem;
  max-width: 900px;
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

.loading,
.error {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 18px;
  font-weight: 600;
  animation: fadeIn 0.4s ease;
}

.empty {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 18px;
  font-weight: 600;
}

.error {
  color: var(--error, #ff4444);
  background: rgba(255, 68, 68, 0.1);
  border-radius: var(--radius-xl, 16px);
  border: 2px solid rgba(255, 68, 68, 0.3);
}

.notificaciones-list {
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
  display: flex;
  gap: 1.5rem;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) backwards;
}

.notificacion-card.no-leida {
  border-left: 4px solid var(--success, #00ff88);
  background: #fff;
}

.notificacion-card:hover {
  transform: translateX(4px);
  border-color: var(--success, #00ff88);
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.4);
}

.notif-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
  filter: drop-shadow(0 0 10px rgba(0, 255, 136, 0.5));
}

.notif-content {
  flex: 1;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.notif-codigo {
  background: var(--success, #00ff88);
  color: #000;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full, 9999px);
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.notif-fecha {
  color: #666;
  font-size: 13px;
  font-weight: 600;
}

.notif-mensaje {
  margin: 0 0 1.5rem 0;
  color: #666;
  line-height: 1.6;
  font-size: 15px;
  font-weight: 500;
}

.btn-marcar-leida {
  padding: 0.75rem 1.5rem;
  background: #fff;
  color: #000;
  border: none;
  border-radius: var(--radius-lg, 12px);
  cursor: pointer;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-marcar-leida::before {
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

.btn-marcar-leida:hover::before {
  width: 300px;
  height: 300px;
}

.btn-marcar-leida:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .notificaciones-content {
    padding: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .notificacion-card {
    padding: 1.5rem;
  }

  .notif-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .notificaciones-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 28px;
  }

  .notif-icon {
    font-size: 2rem;
  }

  .notificacion-card {
    padding: 1.25rem;
    gap: 1rem;
  }
}
</style>
