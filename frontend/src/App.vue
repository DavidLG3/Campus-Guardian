<template>
  <div id="app">
    <router-view v-slot="{ Component, route }">
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
import { onErrorCaptured } from 'vue'

// Capture global errors
onErrorCaptured((err, instance, info) => {
  console.error('Error capturado en App.vue:', err, info)
  // Do not propagate the error to avoid black screens
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

/* Transitions between views */
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
