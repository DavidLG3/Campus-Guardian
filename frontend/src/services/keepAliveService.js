// keepAliveService.js: core module for Campus Guardian frontend.
import api from '@/config/api'

class KeepAliveService {
  constructor() {
    this.intervalId = null
    this.pingInterval = 10 * 60 * 1000 // 10 minutes in milliseconds
  }

  /**
   * Starts the keep-alive service that pings the backend every 10 minutes
   */
  start() {
    if (this.intervalId) {
    console.log('Keep-alive service already running')
      return
    }

    console.log('Starting keep-alive service (ping every 10 minutes)')
    
    // Ping immediately
    this.ping()
    
    // Set up interval for periodic pings
    this.intervalId = setInterval(() => {
      this.ping()
    }, this.pingInterval)
  }

  /**
   * Stops the keep-alive service
   */
  stop() {
    if (this.intervalId) {
      console.log('Stopping keep-alive service')
      clearInterval(this.intervalId)
      this.intervalId = null
    }
  }

  /**
   * Pings the backend to keep it active
   */
  async ping() {
    try {
      // Use a lightweight endpoint that does not require authentication
      // If no health check endpoint exists, use any public GET endpoint
      const response = await api.get('/health/', { timeout: 5000 })
      console.log('Keep-alive ping successful:', new Date().toLocaleTimeString())
      return response.data
    } catch (error) {
      // If the /health/ endpoint does not exist, try another endpoint
      if (error.response?.status === 404) {
        try {
          // Try with an endpoint that surely exists
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
   * Checks if the service is running
   */
  isRunning() {
    return this.intervalId !== null
  }
}

// Export singleton instance
export default new KeepAliveService()
