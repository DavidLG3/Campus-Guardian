// alertaService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Obtener todas las alertas
  getAll(params = {}) {
    return apiClient.get('/alertas/', { params })
  },
  
  // Obtener una alerta por ID
  getById(id) {
    return apiClient.get(`/alertas/${id}/`)
  },
  
  // Crear nueva alerta
  create(alerta) {
    return apiClient.post('/alertas/', alerta)
  },
  
  // Actualizar alerta
  update(id, alerta) {
    return apiClient.put(`/alertas/${id}/`, alerta)
  },
  
  // Eliminar alerta
  delete(id) {
    return apiClient.delete(`/alertas/${id}/`)
  },
  
  // Marcar alerta como leída
  markAsRead(id) {
    return apiClient.patch(`/alertas/${id}/marcar_leida/`)
  },
  
  // Obtener alertas activas
  getActive() {
    return apiClient.get('/alertas/', {
      params: { activa: true }
    })
  },
}
