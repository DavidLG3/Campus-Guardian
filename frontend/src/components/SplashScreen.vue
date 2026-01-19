<template>
  <div class="splash-screen">
    <div class="splash-content">
      <img src="@/assets/portada_aplicacion.png" alt="Portada" class="portada-img" />
      <button class="start-btn" @click="startApp">Empezar</button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['start'])

const startApp = () => {
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  background: #000000;
  position: relative;
  overflow: hidden;
}

.splash-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  z-index: 1;
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

.portada-img {
  max-width: 85vw;
  max-height: 50vh;
  width: auto;
  height: auto;
  display: block;
}

.start-btn {
  padding: 1rem 3.5rem;
  font-size: 1.25rem;
  font-weight: 700;
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

.start-btn::before {
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

.start-btn:hover::before {
  width: 500px;
  height: 500px;
}

.start-btn:hover {
  transform: translateY(-6px) scale(1.08);
  box-shadow: 0 20px 60px rgba(255, 255, 255, 0.5);
  animation: none;
}

.start-btn:active {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 12px 40px rgba(255, 255, 255, 0.4);
}

/* Responsive */
@media (max-width: 768px) {
  .app-title {
    font-size: 48px;
  }
  
  .portada-img {
    max-width: 250px;
  }
  
  .start-btn {
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
  
  .portada-img {
    max-width: 200px;
  }
  
  .start-btn {
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
