import api from '@/config/api'

class KeepAliveService {
  constructor() {
    this.intervalId = null
    this.pingInterval = 10 * 60 * 1000 // 10 minutos en milisegundos
  }

  /**
   * Inicia el servicio de keep-alive que hace ping al backend cada 10 minutos
   */
  start() {
    if (this.intervalId) {
      console.log('Keep-alive service already running')
      return
    }

    console.log('Starting keep-alive service (ping every 10 minutes)')
    
    // Hacer ping inmediatamente
    this.ping()
    
    // Configurar intervalo para pings periódicos
    this.intervalId = setInterval(() => {
      this.ping()
    }, this.pingInterval)
  }

  /**
   * Detiene el servicio de keep-alive
   */
  stop() {
    if (this.intervalId) {
      console.log('Stopping keep-alive service')
      clearInterval(this.intervalId)
      this.intervalId = null
    }
  }

  /**
   * Hace un ping al backend para mantenerlo activo
   */
  async ping() {
    try {
      // Usar un endpoint ligero que no requiera autenticación
      // Si no existe un endpoint de health check, usa cualquier endpoint GET público
      const response = await api.get('/health/', { timeout: 5000 })
      console.log('Keep-alive ping successful:', new Date().toLocaleTimeString())
      return response.data
    } catch (error) {
      // Si el endpoint /health/ no existe, intentar con otro endpoint
      if (error.response?.status === 404) {
        try {
          // Intentar con un endpoint que seguramente existe
          await api.head('/', { timeout: 5000 })
          console.log('Keep-alive ping successful (fallback):', new Date().toLocaleTimeString())
        } catch (fallbackError) {
          console.warn('Keep-alive ping failed:', fallbackError.message)
        }
      } else {
        console.warn('Keep-alive ping failed:', error.message)
      }
    }
  }

  /**
   * Verifica si el servicio está corriendo
   */
  isRunning() {
    return this.intervalId !== null
  }
}

// Exportar instancia singleton
export default new KeepAliveService()
