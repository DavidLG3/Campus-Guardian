import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import alertaService from '@/services/alertaService'

export const useAlertaStore = defineStore('alerta', () => {
  const alertas = ref([])
  const currentAlerta = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const alertasActivas = computed(() => {
    if (!Array.isArray(alertas.value)) return []
    return alertas.value.filter(a => a.activa)
  })

  const alertasNoLeidas = computed(() => {
    if (!Array.isArray(alertas.value)) return []
    return alertas.value.filter(a => !a.leida)
  })

  const countNoLeidas = computed(() => {
    if (!Array.isArray(alertasNoLeidas.value)) return 0
    return alertasNoLeidas.value.length
  })

  async function fetchAll(params = {}) {
    // Solo mostrar loading en la primera carga (cuando no hay alertas)
    const primeraVez = alertas.value.length === 0
    if (primeraVez) {
      isLoading.value = true
      error.value = null
    }
    
    try {
      const response = await alertaService.getAll(params)
      
      if (!response || !response.data) {
        if (primeraVez) {
          alertas.value = []
        }
        return []
      }
      
      // DRF retorna paginación: {count, next, previous, results: []}
      let data = []
      if (response.data.results && Array.isArray(response.data.results)) {
        data = response.data.results
      } else if (Array.isArray(response.data)) {
        data = response.data
      }
      
      // Solo actualizar si hay cambios (nuevas alertas o cambios en leída)
      const hayNuevasAlertas = data.length !== alertas.value.length ||
        data.some(nueva => {
          const existente = alertas.value.find(a => a.id === nueva.id)
          return !existente || existente.leida !== nueva.leida || existente.activa !== nueva.activa
        })
      
      if (hayNuevasAlertas) {
        alertas.value = data
      }
      
      // Limpiar error solo si había uno previo
      if (error.value && primeraVez) {
        error.value = null
      }
      
      return data
    } catch (err) {
      // Solo actualizar error si cambió
      const nuevoError = err.response?.data?.message || 'Error al cargar alertas'
      if (error.value !== nuevoError) {
        error.value = nuevoError
      }
      console.error('Error al cargar alertas:', err)
      if (primeraVez) {
        alertas.value = []
      }
      return []
    } finally {
      if (primeraVez) {
        isLoading.value = false
      }
    }
  }

  async function fetchById(id) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await alertaService.getById(id)
      currentAlerta.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar alerta'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchActive() {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await alertaService.getActive()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar alertas activas'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function create(alerta) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await alertaService.create(alerta)
      alertas.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear alerta'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function update(id, alerta) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await alertaService.update(id, alerta)
      const index = alertas.value.findIndex(a => a.id === id)
      if (index !== -1) {
        alertas.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar alerta'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function remove(id) {
    isLoading.value = true
    error.value = null
    
    try {
      await alertaService.delete(id)
      alertas.value = alertas.value.filter(a => a.id !== id)
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al eliminar alerta'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function markAsRead(id) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await alertaService.markAsRead(id)
      const index = alertas.value.findIndex(a => a.id === id)
      if (index !== -1) {
        alertas.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al marcar alerta como leída'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    alertas,
    currentAlerta,
    isLoading,
    error,
    alertasActivas,
    alertasNoLeidas,
    countNoLeidas,
    fetchAll,
    fetchById,
    fetchActive,
    create,
    update,
    remove,
    markAsRead,
  }
})
