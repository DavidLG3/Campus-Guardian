// usuarioService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Get all users
  getAll(params = {}) {
    return apiClient.get('/usuarios/', { params })
  },
  
  // Get user by ID
  getById(id) {
    return apiClient.get(`/usuarios/${id}/`)
  },
  
  // Update user profile
  updateProfile(id, data) {
    const config = {}
    // If it's FormData (to upload files), set appropriate headers
    if (data instanceof FormData) {
      config.headers = {
        'Content-Type': 'multipart/form-data'
      }
    }
    return apiClient.put(`/usuarios/${id}/`, data, config)
  },
  
  // Change password
  changePassword(oldPassword, newPassword) {
    return apiClient.post('/usuarios/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
    })
  },
}
