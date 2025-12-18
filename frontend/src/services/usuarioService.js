import apiClient from '@/config/api'

export default {
  // Obtener todos los usuarios
  getAll(params = {}) {
    return apiClient.get('/usuarios/', { params })
  },
  
  // Obtener un usuario por ID
  getById(id) {
    return apiClient.get(`/usuarios/${id}/`)
  },
  
  // Actualizar perfil de usuario
  updateProfile(id, data) {
    return apiClient.put(`/usuarios/${id}/`, data)
  },
  
  // Cambiar contraseña
  changePassword(oldPassword, newPassword) {
    return apiClient.post('/usuarios/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
    })
  },
}
