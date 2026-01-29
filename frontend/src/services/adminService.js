import api from '@/config/api'

const adminService = {
  // Listar usuarios con filtro opcional
  async listarUsuarios(tipo = null, search = null) {
    const params = {}
    if (tipo) params.tipo = tipo
    if (search) params.search = search
    
    return api.get('/admin/usuarios/', { params })
  },

  // Crear usuario de seguridad
  async crearUsuarioSeguridad(userData) {
    return api.post('/admin/usuarios/seguridad/', userData)
  },

  // Eliminar usuario
  async eliminarUsuario(userId) {
    return api.delete(`/admin/usuarios/${userId}/`)
  }
}

export default adminService
