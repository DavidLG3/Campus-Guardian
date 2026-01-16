import apiClient from '@/config/api'

export default {
  /**
   * Obtener comentarios de una incidencia
   */
  getComentariosByIncidencia(incidenciaId) {
    return apiClient.get(`/comentarios/`, {
      params: { incidencia: incidenciaId }
    })
  },

  /**
   * Crear un nuevo comentario
   */
  createComentario(data) {
    return apiClient.post('/comentarios/', data)
  },

  /**
   * Eliminar un comentario (solo el autor o admin)
   */
  deleteComentario(id) {
    return apiClient.delete(`/comentarios/${id}/`)
  }
}
