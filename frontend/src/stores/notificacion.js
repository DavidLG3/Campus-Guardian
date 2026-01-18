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
    // Solo mostrar loading en la primera carga (cuando no hay notificaciones)
    const primeraVez = notificaciones.value.length === 0
    if (primeraVez) {
      isLoading.value = true
      error.value = null
    }
    
    try {
      const response = await notificacionService.getAll()
      
      // El API devuelve una respuesta paginada con {count, results}
      const data = response.data.results || response.data || []
      
      // Filtrar elementos null o inválidos
      const nuevasNotificaciones = Array.isArray(data) ? data.filter(n => n && n.id) : []
      
      // Solo actualizar si hay cambios (nuevas notificaciones o cambios en leída)
      const hayNuevasNotificaciones = nuevasNotificaciones.length !== notificaciones.value.length ||
        nuevasNotificaciones.some(nueva => {
          const existente = notificaciones.value.find(n => n.id === nueva.id)
          return !existente || existente.leida !== nueva.leida
        })
      
      if (hayNuevasNotificaciones) {
        notificaciones.value = nuevasNotificaciones
      }
      
      // Limpiar error solo si había uno previo
      if (error.value && primeraVez) {
        error.value = null
      }
      
      return notificaciones.value
    } catch (err) {
      // Solo actualizar error si cambió
      const nuevoError = err.response?.data?.message || 'Error al cargar notificaciones'
      if (error.value !== nuevoError) {
        error.value = nuevoError
      }
      console.error('Error al cargar notificaciones:', err)
      if (primeraVez) {
        notificaciones.value = []
      }
      return []
    } finally {
      if (primeraVez) {
        isLoading.value = false
      }
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
