import axios from 'axios'

// URL base del backend Django
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// Crear instancia de axios
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Interceptor para añadir el token de autenticación
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // Si es FormData, eliminar Content-Type para que el navegador lo establezca automáticamente
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores de respuesta
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Solo limpiar y redirigir si estamos en una ruta protegida
      const currentPath = window.location.pathname
      const publicPaths = ['/login', '/register']
      
      if (!publicPaths.includes(currentPath)) {
        // Token expirado o inválido
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        // Solo redirigir si no estamos ya en login/register
        if (currentPath !== '/login' && currentPath !== '/register') {
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
