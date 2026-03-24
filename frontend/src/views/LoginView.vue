<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Campus Guardian</h1>
      <h2>Iniciar Sesión</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="credentials.email"
            type="email"
            required
            placeholder="tu@email.com"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            required
            placeholder="••••••••"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button type="submit" :disabled="isLoading" class="btn-primary">
          <span>{{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}</span>
        </button>
      </form>
      
      <p class="register-link">
        ¿No tienes cuenta? 
        <router-link to="/register">Regístrate aquí</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  email: '',
  password: ''
})

const error = ref('')
const isLoading = ref(false)

async function handleLogin() {
  error.value = ''
  isLoading.value = true
  
  try {
    await authStore.login(credentials.value)
    
    // Redirigir según el tipo de usuario
    let redirect = router.currentRoute.value.query.redirect
    
    if (!redirect) {
      // Si es admin, ir al dashboard de admin
      if (authStore.isAdmin) {
        redirect = '/admin'
      } else {
        redirect = '/dashboard'
      }
    }
    
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al iniciar sesión'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
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

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #000;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(0, 255, 136, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
  pointer-events: none;
}

.login-container::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 204, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite reverse;
  pointer-events: none;
}

.login-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);
  border: 2px solid rgba(255, 255, 255, 0.1);
  padding: 3rem;
  border-radius: var(--radius-2xl, 20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  width: 100%;
  max-width: 450px;
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.login-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-2xl, 20px);
  padding: 2px;
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.3), rgba(0, 204, 255, 0.3));
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.login-card:hover::before {
  opacity: 1;
}

h1 {
  text-align: center;
  color: #fff;
  margin-bottom: 0.5rem;
  font-size: 48px;
  font-weight: 900;
  letter-spacing: -0.03em;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

h2 {
  text-align: center;
  color: var(--text-secondary, #a0a0a0);
  margin-bottom: 3rem;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.01em;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
}

.form-group {
  margin-bottom: 1.5rem;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.3s backwards;
}

label {
  display: block;
  margin-bottom: 0.75rem;
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

input {
  width: 100%;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg, 12px);
  font-size: 16px;
  color: #fff;
  font-weight: 600;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

input:focus {
  outline: none;
  border-color: var(--success, #00ff88);
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 255, 136, 0.2);
}

.error-message {
  background: linear-gradient(135deg, rgba(255, 68, 68, 0.2) 0%, rgba(255, 68, 68, 0.1) 100%);
  color: var(--error, #ff4444);
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg, 12px);
  border: 2px solid rgba(255, 68, 68, 0.3);
  margin-bottom: 1.5rem;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.01em;
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary {
  width: 100%;
  padding: 1rem 1.5rem;
  background: #fff;
  color: #000;
  border: none;
  border-radius: var(--radius-lg, 12px);
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.4s backwards;
}

.btn-primary::before {
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
}

.btn-primary:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary span {
  position: relative;
  z-index: 1;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(255, 255, 255, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.btn-primary:disabled:hover {
  transform: none;
  box-shadow: none;
}

.btn-primary:disabled::before {
  display: none;
}

.register-link {
  text-align: center;
  margin-top: 2rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 14px;
  font-weight: 600;
  animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.5s backwards;
}

.register-link a {
  color: var(--success, #00ff88);
  text-decoration: none;
  font-weight: 800;
  letter-spacing: 0.02em;
  transition: all var(--transition-fast, 0.15s);
  position: relative;
}

.register-link a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--success, #00ff88);
  transition: width var(--transition-base, 0.3s);
}

.register-link a:hover {
  color: #fff;
}

.register-link a:hover::after {
  width: 100%;
}
</style>
