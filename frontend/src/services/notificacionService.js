// notificacionService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Get all user notifications
  getAll() {
    return apiClient.get('/notificaciones/')
  },
  
  // Get notification by ID
  getById(id) {
    return apiClient.get(`/notificaciones/${id}/`)
  },
  
  // Mark notification as read
  markAsRead(id) {
    return apiClient.patch(`/notificaciones/${id}/marcar_leida/`)
  },
  
  // Get unread notifications
  getUnread() {
    return apiClient.get('/notificaciones/no_leidas/')
  },
  
  // Count unread notifications
  countUnread() {
    return apiClient.get('/notificaciones/count_no_leidas/')
  }
}
