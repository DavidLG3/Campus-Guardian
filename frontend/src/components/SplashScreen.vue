<template>
  <div v-if="isVisible" class="splash-screen">
    <div class="splash-content">
      <img 
        src="/logo2.jpg" 
        alt="Logo Campus Guardian" 
        class="splash-logo"
        @error="handleImageError"
        @load="handleImageLoad"
      />
      <button @click="handleStart" class="start-button">
        START
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['start'])
const isVisible = ref(true)

const handleStart = () => {
  isVisible.value = false
  emit('start')
}

const handleImageError = (e) => {
  console.error('Error cargando logo:', e)
  // Si falla la carga, seguir mostrando el botón
}

const handleImageLoad = () => {
  console.log('Logo cargado correctamente')
}
</script>

<style scoped>
.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.splash-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  width: 90%;
  max-width: 600px;
}

.splash-logo {
  max-width: 80vw;
  max-height: 60vh;
  width: auto;
  height: auto;
  object-fit: contain;
  animation: logoScale 1s ease-in-out;
}

@keyframes logoScale {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.start-button {
  margin-top: 2rem;
  padding: 1rem 3rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  text-transform: uppercase;
  letter-spacing: 2px;
}

.start-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.start-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .start-button {
    font-size: 1.2rem;
    padding: 0.8rem 2.5rem;
  }
}

@media (max-width: 480px) {
  .start-button {
    font-size: 1rem;
    padding: 0.7rem 2rem;
  }
}
</style>
