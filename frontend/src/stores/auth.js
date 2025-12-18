import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  // Getters (con validación defensiva)
  const isAuthenticated = computed(() => {
    try {
      return !!token.value
    } catch (err) {
      console.error('Error en isAuthenticated:', err)
      return false
    }
  })
  
  const userRole = computed(() => {
    try {
      return user.value?.rol || null
    } catch (err) {
      console.error('Error en userRole:', err)
      return null
    }
  })
  
  const isAdmin = computed(() => {
    try {
      return userRole.value === 'admin'
    } catch (err) {
      console.error('Error en isAdmin:', err)
      return false
    }
  })
  
  const isOperador = computed(() => {
    try {
      return userRole.value === 'operador'
    } catch (err) {
      console.error('Error en isOperador:', err)
      return false
    }
  })
  
  const isCiudadano = computed(() => {
    try {
      return userRole.value === 'ciudadano'
    } catch (err) {
      console.error('Error en isCiudadano:', err)
      return false
    }
  })

  // Actions
  async function login(credentials) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authService.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      
      // Guardar en localStorage
      localStorage.setItem('token', token.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al iniciar sesión'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function register(userData) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authService.register(userData)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al registrarse'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    // No hay endpoint de logout en backend, solo limpiamos el estado local
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchCurrentUser() {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await authService.getCurrentUser()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al obtener usuario'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function loadFromLocalStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      try {
        user.value = JSON.parse(savedUser)
      } catch (err) {
        console.error('Error parsing user data:', err)
        logout()
      }
    }
  }

  // Cargar datos al iniciar
  loadFromLocalStorage()

  return {
    // State
    user,
    token,
    isLoading,
    error,
    // Getters
    isAuthenticated,
    userRole,
    isAdmin,
    isOperador,
    isCiudadano,
    // Actions
    login,
    register,
    logout,
    fetchCurrentUser,
    loadFromLocalStorage,
  }
})
