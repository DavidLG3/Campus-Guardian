import apiClient from '@/config/api'

export default {
  // Obtener todas las notificaciones del usuario
  getAll() {
    return apiClient.get('/notificaciones/')
  },
  
  // Obtener una notificación por ID
  getById(id) {
    return apiClient.get(`/notificaciones/${id}/`)
  },
  
  // Marcar notificación como leída
  markAsRead(id) {
    return apiClient.patch(`/notificaciones/${id}/marcar_leida/`)
  },
  
  // Obtener notificaciones no leídas
  getUnread() {
    return apiClient.get('/notificaciones/no_leidas/')
  },
  
  // Contar notificaciones no leídas
  countUnread() {
    return apiClient.get('/notificaciones/count_no_leidas/')
  }
}
