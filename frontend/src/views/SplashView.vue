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
    // Check if there is a token in cookies/localStorage
    const token = localStorage.getItem('token')
    
    if (token && authStore.isAuthenticated) {
      // If there is an active session, go to the dashboard.
      await router.replace('/dashboard')
    } else {
      // If there is no session, stay on the initial route.
      await router.replace('/')
    }
  } catch (error) {
    console.error('Error en handleStart:', error)
    // In case of error, fall back to the initial route.
    router.replace('/')
  }
}
</script>
