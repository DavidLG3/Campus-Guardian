import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import keepAliveService from './services/keepAliveService'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// Iniciar el servicio de keep-alive para mantener el backend activo en Render
// Solo en producción para evitar pings innecesarios en desarrollo
if (import.meta.env.PROD) {
  keepAliveService.start()
  console.log('Keep-alive service started for production')
}
