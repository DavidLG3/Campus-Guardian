import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import notificacionService from '@/services/notificacionService'

export const useNotificacionStore = defineStore('notificacion', () => {
  const notificaciones = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  const countNoLeidas = computed(() => {
    try {
      if (!Array.isArray(notificaciones.value)) {
        return 0
      }
      return notificaciones.value.filter(n => n && n.id && !n.leida).length
    } catch (err) {
      console.error('Error calculando notificaciones no leídas:', err)
      return 0
    }
  })

  async function fetchAll() {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await notificacionService.getAll()
      console.log('[STORE] Respuesta del API:', response)
      console.log('[STORE] Datos recibidos:', response.data)
      
      // El API devuelve una respuesta paginada con {count, results}
      const data = response.data.results || response.data || []
      
      // Filtrar elementos null o inválidos
      notificaciones.value = Array.isArray(data) ? data.filter(n => n && n.id) : []
      console.log('[STORE] Notificaciones guardadas en store:', notificaciones.value)
      console.log('[STORE] Cantidad de notificaciones:', notificaciones.value.length)
      return notificaciones.value
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar notificaciones'
      console.error('Error al cargar notificaciones:', err)
      notificaciones.value = []
      return []
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUnread() {
    try {
      const response = await notificacionService.getUnread()
      return response.data || []
    } catch (err) {
      console.error('Error al cargar notificaciones no leídas:', err)
      return []
    }
  }

  async function markAsRead(id) {
    try {
      const response = await notificacionService.markAsRead(id)
      const index = notificaciones.value.findIndex(n => n.id === id)
      if (index !== -1) {
        notificaciones.value[index].leida = true
      }
      return response.data
    } catch (err) {
      console.error('Error al marcar notificación como leída:', err)
      throw err
    }
  }

  async function fetchCount() {
    try {
      const response = await notificacionService.countUnread()
      return response.data?.count || 0
    } catch (err) {
      console.error('Error al contar notificaciones:', err)
      return 0
    }
  }

  return {
    notificaciones,
    isLoading,
    error,
    countNoLeidas,
    fetchAll,
    fetchUnread,
    markAsRead,
    fetchCount
  }
})
