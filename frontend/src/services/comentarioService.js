// comentarioService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  /**
   * Get comments from an incident
   */
  getComentariosByIncidencia(incidenciaId) {
    return apiClient.get(`/comentarios/`, {
      params: { incidencia: incidenciaId }
    })
  },

  /**
   * Create a new comment
   */
  createComentario(data) {
    return apiClient.post('/comentarios/', data)
  },

  /**
   * Delete a comment (only author or admin)
   */
  deleteComentario(id) {
    return apiClient.delete(`/comentarios/${id}/`)
  }
}
