<template>
  <div v-if="isVisible" class="splash-screen">
    <div class="splash-content">
      <div class="logo-container">
        <img 
          src="https://cdn-icons-gif.flaticon.com/15576/15576868.gif" 
          alt="Camera Security Icon" 
          class="camera-icon"
        />
        <h1 class="app-title">Campus Guardian</h1>
      </div>
      <button @click="handleStart" class="start-button">
        <span>START</span>
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
</script>

<style scoped>
@keyframes fadeInUp {
  0% {
    transform: translateY(30px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7);
  }
  50% {
    box-shadow: 0 0 0 25px rgba(0, 255, 136, 0);
  }
}

@keyframes rotateIcon {
  0% {
    transform: rotate(0deg) scale(1);
  }
  50% {
    transform: rotate(5deg) scale(1.1);
  }
  100% {
    transform: rotate(0deg) scale(1);
  }
}

.splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  overflow: hidden;
}

.splash-screen::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(0, 255, 136, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite;
  pointer-events: none;
}

.splash-screen::after {
  content: '';
  position: absolute;
  bottom: -50%;
  left: -20%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(0, 204, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 10s ease-in-out infinite reverse;
  pointer-events: none;
}

.splash-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5rem;
  width: 90%;
  max-width: 800px;
  position: relative;
  z-index: 1;
}

.logo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  animation: fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.camera-icon {
  width: 150px;
  height: 150px;
  filter: drop-shadow(0 0 40px rgba(0, 255, 136, 0.6));
  animation: float 3s ease-in-out infinite;
}

.app-title {
  font-size: 72px;
  font-weight: 900;
  color: #fff;
  letter-spacing: -0.04em;
  text-align: center;
  line-height: 1;
  text-transform: uppercase;
  background: linear-gradient(135deg, #fff 0%, var(--success, #00ff88) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 40px rgba(0, 255, 136, 0.3));
}

.start-button {
  padding: 1.75rem 6rem;
  font-size: 2rem;
  font-weight: 900;
  color: #000;
  background: #fff;
  border: none;
  border-radius: var(--radius-full, 9999px);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 15px 50px rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  position: relative;
  overflow: hidden;
  animation: pulse 2.5s ease-in-out infinite, fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1) 0.3s backwards;
}

.start-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--success, #00ff88);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.start-button span {
  position: relative;
  z-index: 1;
}

.start-button:hover::before {
  width: 500px;
  height: 500px;
}

.start-button:hover {
  transform: translateY(-6px) scale(1.08);
  box-shadow: 0 20px 60px rgba(255, 255, 255, 0.5);
  animation: none;
}

.start-button:active {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 12px 40px rgba(255, 255, 255, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .app-title {
    font-size: 48px;
  }
  
  .camera-icon {
    width: 110px;
    height: 110px;
  }
  
  .start-button {
    font-size: 1.5rem;
    padding: 1.25rem 4rem;
  }
  
  .splash-content {
    gap: 4rem;
  }
  
  .splash-screen::before,
  .splash-screen::after {
    width: 400px;
    height: 400px;
  }
}

@media (max-width: 480px) {
  .app-title {
    font-size: 36px;
  }
  
  .camera-icon {
    width: 90px;
    height: 90px;
  }
  
  .start-button {
    font-size: 1.25rem;
    padding: 1rem 3rem;
  }
  
  .splash-content {
    gap: 3rem;
  }
  
  .logo-container {
    gap: 1.5rem;
  }
}
</style>
