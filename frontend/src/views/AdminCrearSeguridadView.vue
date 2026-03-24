<template>
  <AppLayout>
    <div class="crear-seguridad">
      <div class="form-container">
        <h1>Crear Usuario de Seguridad</h1>
        <p class="subtitle">Complete el formulario para dar de alta a un nuevo miembro del personal de seguridad</p>

        <form @submit.prevent="handleSubmit" class="form">
          <div v-if="error" class="alert alert-error">{{ error }}</div>
          <div v-if="success" class="alert alert-success">{{ success }}</div>

          <div class="form-row">
            <div class="form-group">
              <label for="first_name">Nombre *</label>
              <input
                id="first_name"
                v-model="formData.first_name"
                type="text"
                required
                placeholder="Ej: Juan"
              />
            </div>

            <div class="form-group">
              <label for="last_name">Apellidos *</label>
              <input
                id="last_name"
                v-model="formData.last_name"
                type="text"
                required
                placeholder="Ej: Pérez García"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="username">Nombre de usuario *</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              placeholder="Ej: juan.perez"
              pattern="[a-zA-Z0-9._-]{3,30}"
            />
            <small class="help-text">Solo letras, números, puntos, guiones y guiones bajos. Mínimo 3 caracteres.</small>
          </div>

          <div class="form-group">
            <label for="email">Correo electrónico *</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              placeholder="Ej: juan.perez@seguridad.com"
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
            <small class="help-text">Opcional. Formato: +34 600 000 000</small>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="password">Contraseña *</label>
              <input
                id="password"
                v-model="formData.password"
                type="password"
                required
                minlength="6"
                placeholder="••••••••"
              />
              <small class="help-text">Mínimo 6 caracteres</small>
            </div>

            <div class="form-group">
              <label for="password2">Confirmar contraseña *</label>
              <input
                id="password2"
                v-model="formData.password2"
                type="password"
                required
                placeholder="••••••••"
              />
            </div>
          </div>

          <div class="credentials-info">
            <h3>📋 Información importante</h3>
            <p>Estos serán los datos de acceso del usuario. Asegúrate de proporcionarlos de forma segura al personal de seguridad.</p>
          </div>

          <div class="form-actions">
            <button type="button" @click="$router.back()" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" :disabled="isLoading" class="btn-primary">
              {{ isLoading ? 'Creando...' : 'Crear Usuario' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import adminService from '@/services/adminService'
import AppLayout from '@/layouts/AppLayout.vue'

const router = useRouter()

const formData = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: '',
  last_name: '',
  telefono: ''
})

const isLoading = ref(false)
const error = ref(null)
const success = ref(null)

async function handleSubmit() {
  error.value = null
  success.value = null

  // Validations
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
    const response = await adminService.crearUsuarioSeguridad(formData.value)
    success.value = 'Usuario de seguridad creado exitosamente'
    
    // Clean formulary
    formData.value = {
      username: '',
      email: '',
      password: '',
      password2: '',
      first_name: '',
      last_name: '',
      telefono: ''
    }

    // Redirect after 2 seconds
    setTimeout(() => {
      router.push('/admin/usuarios')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al crear usuario de seguridad'
    console.error('Error:', err)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.crear-seguridad {
  padding: 2rem;
  background: #000;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.form-container {
  background: #111;
  border: 2px solid #222;
  border-radius: 20px;
  padding: 3rem;
  max-width: 800px;
  width: 100%;
  margin-top: 2rem;
}

h1 {
  font-size: 36px;
  font-weight: 900;
  color: #fff;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.subtitle {
  color: #999;
  font-size: 16px;
  margin-bottom: 2rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #fff;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-group input {
  padding: 1rem 1.5rem;
  background: #000;
  border: 2px solid #222;
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1);
}

.help-text {
  font-size: 12px;
  color: #666;
  font-style: italic;
}

.credentials-info {
  background: #1a1a1a;
  border: 2px solid #00ccff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1rem;
}

.credentials-info h3 {
  font-size: 16px;
  font-weight: 700;
  color: #00ccff;
  margin: 0 0 0.5rem 0;
}

.credentials-info p {
  font-size: 14px;
  color: #999;
  margin: 0;
  line-height: 1.5;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

.btn-primary,
.btn-secondary {
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.btn-primary {
  background: #00ff88;
  color: #000;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #222;
  color: #fff;
  border: 2px solid #333;
}

.btn-secondary:hover {
  border-color: #00ff88;
}

.alert {
  padding: 1rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
}

.alert-error {
  background: rgba(255, 68, 68, 0.1);
  border: 2px solid #ff4444;
  color: #ff4444;
}

.alert-success {
  background: rgba(0, 255, 136, 0.1);
  border: 2px solid #00ff88;
  color: #00ff88;
}

@media (max-width: 768px) {
  .crear-seguridad {
    padding: 1rem;
  }

  .form-container {
    padding: 2rem;
  }

  h1 {
    font-size: 28px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
