// incidenciaService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Obtener todas las incidencias
  getAll(params = {}) {
    return apiClient.get('/incidencias/', { params })
  },
  
  // Obtener una incidencia por ID
  getById(id) {
    return apiClient.get(`/incidencias/${id}/`)
  },
  
  // Crear nueva incidencia
  create(incidencia) {
    return apiClient.post('/incidencias/', incidencia)
  },
  
  // Actualizar incidencia
  update(id, incidencia) {
    return apiClient.put(`/incidencias/${id}/`, incidencia)
  },
  
  // Eliminar incidencia
  delete(id) {
    return apiClient.delete(`/incidencias/${id}/`)
  },
  
  // Cambiar estado de incidencia
  updateEstado(id, estado) {
    return apiClient.patch(`/incidencias/${id}/cambiar_estado/`, { estado })
  },
  
  // Resolver incidencia con nota (personal de seguridad)
  resolver(id, nota_resolucion) {
    return apiClient.post(`/incidencias/${id}/resolver/`, { nota_resolucion })
  },
  
  // Obtener incidencias por área geográfica
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
