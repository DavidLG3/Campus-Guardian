<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Campus Guardian</h1>
      <h2>Crear Cuenta</h2>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="nombre">Nombre completo</label>
          <input
            id="nombre"
            v-model="formData.nombre"
            type="text"
            required
            placeholder="Juan Pérez"
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            placeholder="tu@email.com"
          />
        </div>
        
        <div class="form-group">
          <label for="telefono">Teléfono</label>
          <input
            id="telefono"
            v-model="formData.telefono"
            type="tel"
            placeholder="+34 600 000 000"
          />
        </div>
        
        <div class="form-group">
          <label for="rol">Tipo de usuario</label>
          <select id="rol" v-model="formData.rol" required>
            <option value="">Selecciona un tipo</option>
            <option value="ciudadano">Ciudadano</option>
            <option value="operador">Personal de Seguridad</option>
          </select>
          <small class="help-text">
            • Ciudadano: Puede reportar y ver incidencias<br>
            • Personal de Seguridad: Además puede gestionar alertas
          </small>
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            placeholder="••••••••"
          />
        </div>
        
        <div class="form-group">
          <label for="password2">Confirmar contraseña</label>
          <input
            id="password2"
            v-model="formData.password2"
            type="password"
            required
            placeholder="••••••••"
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          {{ success }}
        </div>
        
        <button type="submit" :disabled="isLoading" class="btn-primary">
          {{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}
        </button>
      </form>
      
      <p class="login-link">
        ¿Ya tienes cuenta? 
        <router-link to="/login">Inicia sesión aquí</router-link>
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

const formData = ref({
  nombre: '',
  email: '',
  telefono: '',
  rol: '',
  password: '',
  password2: ''
})

const error = ref('')
const success = ref('')
const isLoading = ref(false)

async function handleRegister() {
  error.value = ''
  success.value = ''
  
  // Validar contraseñas
  if (formData.value.password !== formData.value.password2) {
    error.value = 'Las contraseñas no coinciden'
    return
  }
  
  if (formData.value.password.length < 6) {
    error.value = 'La contraseña debe tener al menos 6 caracteres'
    return
  }
  
  isLoading.value = true
  
  try {
    await authStore.register({
      nombre: formData.value.nombre,
      email: formData.value.email,
      telefono: formData.value.telefono,
      rol: formData.value.rol,
      password: formData.value.password
    })
    
    success.value = 'Cuenta creada exitosamente. Redirigiendo...'
    
    // Esperar un momento y redirigir al login
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al crear la cuenta'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

h2 {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

input,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

.help-text {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #666;
  line-height: 1.4;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.success-message {
  background-color: #efe;
  color: #3c3;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
