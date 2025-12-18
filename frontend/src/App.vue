<template>
  <div id="app">
    <SplashScreen v-if="showSplash" @start="handleStart" />
    <router-view v-else v-slot="{ Component, route }">
      <Suspense>
        <template #default>
          <transition name="fade" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </transition>
        </template>
        <template #fallback>
          <div class="loading-screen">
            <div class="spinner"></div>
            <p>Cargando...</p>
          </div>
        </template>
      </Suspense>
    </router-view>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SplashScreen from '@/components/SplashScreen.vue'

const router = useRouter()
const authStore = useAuthStore()
const showSplash = ref(true)

const handleStart = async () => {
  showSplash.value = false
  
  try {
    // Verificar si hay token en cookies/localStorage
    const token = localStorage.getItem('token')
    
    if (token && authStore.isAuthenticated) {
      // Si hay sesión activa, ir al dashboard
      await router.push('/dashboard')
    } else {
      // Si no hay sesión, ir al login
      await router.push('/login')
    }
  } catch (error) {
    console.error('Error en handleStart:', error)
    // En caso de error, ir al login
    router.push('/login')
  }
}

// Capturar errores globales
onErrorCaptured((err, instance, info) => {
  console.error('Error capturado en App.vue:', err, info)
  // No propagar el error para evitar pantallas en negro
  return false
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.view-container {
  min-height: 100vh;
}

/* Transiciones entre vistas */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.loading-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-screen p {
  margin-top: 1rem;
  color: #666;
  font-size: 1.1rem;
}
</style>
