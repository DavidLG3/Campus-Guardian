// incidencia.js: core module for Campus Guardian frontend.
import { defineStore } from 'pinia'
import { ref } from 'vue'
import incidenciaService from '@/services/incidenciaService'

export const useIncidenciaStore = defineStore('incidencia', () => {
  const incidencias = ref([])
  const currentIncidencia = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  async function fetchAll(params = {}) {
    isLoading.value = true
    error.value = null
    
    try {
      // DRF paginates results by default, so we fetch every page to avoid
      // showing only the first 10 incidents in the UI.
      let page = 1
      let allIncidencias = []
      let hasNextPage = true

      while (hasNextPage) {
        const response = await incidenciaService.getAll({ ...params, page })

        if (!response || !response.data) {
          break
        }

        let pageData = []
        if (response.data.results && Array.isArray(response.data.results)) {
          pageData = response.data.results
        } else if (Array.isArray(response.data)) {
          pageData = response.data
        }

        allIncidencias = [...allIncidencias, ...pageData]
        hasNextPage = Boolean(response.data.next)
        page += 1

        // If the API is not paginated, stop after the first response.
        if (Array.isArray(response.data)) {
          break
        }
      }

      incidencias.value = allIncidencias
      return allIncidencias
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar incidencias'
      console.error('Error al cargar incidencias:', err)
      incidencias.value = []
      return []
    } finally {
      isLoading.value = false
    }
  }

  async function fetchById(id) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await incidenciaService.getById(id)
      currentIncidencia.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al cargar incidencia'
      console.error('Error en fetchById incidencia:', err)
      currentIncidencia.value = null
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function create(incidencia) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await incidenciaService.create(incidencia)
      // Agregar la nueva incidencia al principio del array para reactividad
      incidencias.value = [response.data, ...incidencias.value]
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al crear incidencia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function update(id, incidencia) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await incidenciaService.update(id, incidencia)
      const index = incidencias.value.findIndex(i => i.id === id)
      if (index !== -1) {
        incidencias.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar incidencia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function remove(id) {
    isLoading.value = true
    error.value = null
    
    try {
      await incidenciaService.delete(id)
      incidencias.value = incidencias.value.filter(i => i.id !== id)
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al eliminar incidencia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function updateEstado(id, estado) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await incidenciaService.updateEstado(id, estado)
      const index = incidencias.value.findIndex(i => i.id === id)
      if (index !== -1) {
        incidencias.value[index] = response.data
      }
      if (currentIncidencia.value && currentIncidencia.value.id === id) {
        currentIncidencia.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al actualizar estado'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function resolver(id, nota_resolucion) {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await incidenciaService.resolver(id, nota_resolucion)
      const index = incidencias.value.findIndex(i => i.id === id)
      if (index !== -1) {
        incidencias.value[index] = response.data
      }
      if (currentIncidencia.value && currentIncidencia.value.id === id) {
        currentIncidencia.value = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Error al resolver incidencia'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    incidencias,
    currentIncidencia,
    isLoading,
    error,
    fetchAll,
    fetchById,
    create,
    update,
    remove,
    updateEstado,
    resolver,
  }
})
