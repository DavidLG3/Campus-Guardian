// alertaService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Get all alerts
  getAll(params = {}) {
    return apiClient.get('/alertas/', { params })
  },
  
  // Get alert by ID
  getById(id) {
    return apiClient.get(`/alertas/${id}/`)
  },
  
  // Create new alert
  create(alerta) {
    return apiClient.post('/alertas/', alerta)
  },
  
  // Update alert
  update(id, alerta) {
    return apiClient.put(`/alertas/${id}/`, alerta)
  },
  
  // Delete alert
  delete(id) {
    return apiClient.delete(`/alertas/${id}/`)
  },
  
  // Mark alert as read
  markAsRead(id) {
    return apiClient.patch(`/alertas/${id}/marcar_leida/`)
  },
  
  // Get active alerts
  getActive() {
    return apiClient.get('/alertas/', {
      params: { activa: true }
    })
  },
}
