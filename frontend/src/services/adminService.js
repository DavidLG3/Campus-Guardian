// adminService.js: core module for Campus Guardian frontend.
import api from '@/config/api'

const adminService = {
  // List users with optional filter
  async listarUsuarios(tipo = null, search = null) {
    const params = {}
    if (tipo) params.tipo = tipo
    if (search) params.search = search
    
    return api.get('/admin/usuarios/', { params })
  },

  // Create security staff user
  async crearUsuarioSeguridad(userData) {
    return api.post('/admin/usuarios/seguridad/', userData)
  },

  // Delete user
  async eliminarUsuario(userId) {
    return api.delete(`/admin/usuarios/${userId}/`)
  }
}

export default adminService
