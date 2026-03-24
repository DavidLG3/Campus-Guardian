// incidenciaService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Get all incidents
  getAll(params = {}) {
    return apiClient.get('/incidencias/', { params })
  },
  
  // Get incident by ID
  getById(id) {
    return apiClient.get(`/incidencias/${id}/`)
  },
  
  // Create new incident
  create(incidencia) {
    return apiClient.post('/incidencias/', incidencia)
  },
  
  // Update incident
  update(id, incidencia) {
    return apiClient.put(`/incidencias/${id}/`, incidencia)
  },
  
  // Delete incident
  delete(id) {
    return apiClient.delete(`/incidencias/${id}/`)
  },
  
  // Change incident status
  updateEstado(id, estado) {
    return apiClient.patch(`/incidencias/${id}/cambiar_estado/`, { estado })
  },
  
  // Resolve incident with note (security staff)
  resolver(id, nota_resolucion) {
    return apiClient.post(`/incidencias/${id}/resolver/`, { nota_resolucion })
  },
  
  // Get incidents by geographic area
  getByArea(latMin, latMax, lonMin, lonMax) {
    return apiClient.get('/incidencias/', {
      params: {
        lat_min: latMin,
        lat_max: latMax,
        lon_min: lonMin,
        lon_max: lonMax,
      }
    })
  },
}
