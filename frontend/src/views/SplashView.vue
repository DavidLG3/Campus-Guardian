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
      // If there is an active session, send admins to the admin panel.
      await router.replace(authStore.isAdmin ? '/admin' : '/dashboard')
    } else {
      // If there is no session, go to the login screen.
      await router.replace('/login')
    }
  } catch (error) {
    console.error('Error en handleStart:', error)
    // In case of error, fall back to the login screen.
    router.replace('/login')
  }
}
</script>
