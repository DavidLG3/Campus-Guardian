<template>
  <SplashScreen @start="handleStart" />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import SplashScreen from '@/components/SplashScreen.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleStart = async () => {
  try {
    // Verificar si hay token en cookies/localStorage
    const token = localStorage.getItem('token')
    
    if (token && authStore.isAuthenticated) {
      // Si hay sesión activa, ir al dashboard
      await router.replace('/dashboard')
    } else {
      // Si no hay sesión, ir al login
      await router.replace('/login')
    }
  } catch (error) {
    console.error('Error en handleStart:', error)
    // En caso de error, ir al login
    router.replace('/login')
  }
}
</script>
