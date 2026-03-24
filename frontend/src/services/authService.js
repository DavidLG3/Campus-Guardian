// authService.js: core module for Campus Guardian frontend.
import apiClient from '@/config/api'

export default {
  // Authentication
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },
  
  register(userData) {
    return apiClient.post('/auth/register/', userData)
  },
  
  logout() {
    return apiClient.post('/auth/logout/')
  },
  
  getCurrentUser() {
    return apiClient.get('/auth/user/')
  },
  
  refreshToken(token) {
    return apiClient.post('/auth/refresh/', { token })
  },
}
