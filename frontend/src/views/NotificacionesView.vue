<template>
  <div class="notificaciones-view">
    <AppLayout>
      <div class="notificaciones-content">
        <h1>🔔 Mis Notificaciones</h1>
        
        <div v-if="isLoading" class="loading">Cargando notificaciones...</div>
        
        <div v-else-if="error" class="error">{{ error }}</div>
        
        <div v-else-if="notificaciones.length === 0" class="empty">
          <p>No tienes notificaciones</p>
        </div>
        
        <div v-else class="notificaciones-list">
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

const notificaciones = computed(() => {
  // Filtrar elementos null o inválidos
  const notifs = notificacionStore.notificaciones
  console.log('[VIEW] Notificaciones del store:', notifs)
  if (!Array.isArray(notifs)) {
    console.log('[VIEW] No es un array, retornando vacío')
    return []
  }
  const filtered = notifs.filter(n => n && n.id)
  console.log('[VIEW] Notificaciones filtradas:', filtered)
  return filtered
})

const isLoading = computed(() => notificacionStore.isLoading)
const error = computed(() => notificacionStore.error)

function formatDate(dateString) {
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
    await notificacionStore.markAsRead(id)
  } catch (err) {
    console.error('Error al marcar notificación como leída:', err)
  }
}

onMounted(() => {
  notificacionStore.fetchAll()
})
</script>

<style scoped>
.notificaciones-content {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.notificaciones-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notificacion-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
  transition: all 0.3s ease;
}

.notificacion-card.no-leida {
  border-left: 4px solid #667eea;
  background: #f8f9ff;
}

.notificacion-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.notif-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.notif-codigo {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
}

.notif-fecha {
  color: #999;
  font-size: 0.85rem;
}

.notif-mensaje {
  margin: 0 0 1rem 0;
  color: #333;
  line-height: 1.5;
}

.btn-marcar-leida {
  padding: 0.5rem 1rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-marcar-leida:hover {
  opacity: 0.9;
}

/* Responsive */
@media (max-width: 768px) {
  .notificaciones-content {
    padding: 1rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .notificacion-card {
    padding: 1rem;
  }

  .notif-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .notificaciones-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 1.25rem;
  }

  .notif-icon {
    font-size: 1.5rem;
  }
}
</style>
