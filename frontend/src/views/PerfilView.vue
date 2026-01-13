<template>
  <div class="perfil-view">
    <AppLayout>
      <div class="perfil-content">
        <h1>Mi Perfil</h1>
        
        <div class="perfil-card">
          <div v-if="isLoading" class="loading">Cargando...</div>
          
          <div v-else>
            <div class="info-section">
              <h2>Información Personal</h2>
              <div class="info-grid">
                <div class="info-item">
                  <label>Nombre:</label>
                  <p>{{ authStore.user?.nombre }}</p>
                </div>
                <div class="info-item">
                  <label>Email:</label>
                  <p>{{ authStore.user?.email }}</p>
                </div>
                <div class="info-item">
                  <label>Teléfono:</label>
                  <p>{{ authStore.user?.telefono || 'No especificado' }}</p>
                </div>
                <div class="info-item">
                  <label>Rol:</label>
                  <p>{{ formatRole(authStore.userRole) }}</p>
                </div>
              </div>
            </div>
            
            <div class="actions">
              <button @click="toggleEditForm" class="btn-secondary">
                {{ showEditForm ? 'Cancelar' : 'Editar Perfil' }}
              </button>
            </div>
            
            <div v-if="showEditForm" class="edit-form">
              <h2>Editar Información</h2>
              
              <form @submit.prevent="handleSubmit">
                <div class="form-group">
                  <label>Nombre:</label>
                  <input 
                    v-model="formData.nombre" 
                    type="text" 
                    placeholder="Tu nombre completo"
                    required
                  />
                </div>

                <div class="form-group">
                  <label>Email:</label>
                  <input 
                    v-model="formData.email" 
                    type="email" 
                    placeholder="tu@email.com"
                    required
                  />
                </div>

                <div class="form-group">
                  <label>Teléfono:</label>
                  <input 
                    v-model="formData.telefono" 
                    type="tel" 
                    placeholder="600123456"
                  />
                </div>

                <div class="form-group">
                  <label>Nueva Contraseña (opcional):</label>
                  <input 
                    v-model="formData.password" 
                    type="password" 
                    placeholder="Dejar vacío para no cambiar"
                  />
                  <small v-if="formData.password" class="helper-text">
                    La contraseña debe ser diferente a la anterior
                  </small>
                </div>

                <div class="form-group">
                  <label>Confirmar Contraseña:</label>
                  <input 
                    v-model="formData.confirmPassword" 
                    type="password" 
                    placeholder="Confirmar nueva contraseña"
                    :disabled="!formData.password"
                  />
                </div>

                <div v-if="error" class="error-message">
                  {{ error }}
                </div>

                <div v-if="success" class="success-message">
                  {{ success }}
                </div>

                <div class="form-actions">
                  <button type="submit" class="btn-primary" :disabled="isSaving">
                    {{ isSaving ? 'Guardando...' : 'Guardar Cambios' }}
                  </button>
                  <button type="button" @click="toggleEditForm" class="btn-cancel">
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import usuarioService from '@/services/usuarioService'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const isLoading = ref(false)
const showEditForm = ref(false)
const isSaving = ref(false)
const error = ref('')
const success = ref('')

const formData = reactive({
  nombre: '',
  email: '',
  telefono: '',
  password: '',
  confirmPassword: ''
})

function formatRole(role) {
  const roles = {
    'admin': 'Administrador',
    'operador': 'Operador',
    'ciudadano': 'Ciudadano'
  }
  return roles[role] || role
}

function toggleEditForm() {
  showEditForm.value = !showEditForm.value
  error.value = ''
  success.value = ''
  
  if (showEditForm.value) {
    // Cargar datos actuales en el formulario
    formData.nombre = authStore.user?.nombre || ''
    formData.email = authStore.user?.email || ''
    formData.telefono = authStore.user?.telefono || ''
    formData.password = ''
    formData.confirmPassword = ''
  }
}

async function handleSubmit() {
  error.value = ''
  success.value = ''
  
  // Validación de contraseñas
  if (formData.password) {
    if (formData.password.length < 6) {
      error.value = 'La contraseña debe tener al menos 6 caracteres'
      return
    }
    
    if (formData.password !== formData.confirmPassword) {
      error.value = 'Las contraseñas no coinciden'
      return
    }
  }
  
  isSaving.value = true
  
  try {
    const updateData = {
      nombre: formData.nombre,
      email: formData.email,
      telefono: formData.telefono || null
    }
    
    // Solo incluir contraseña si se especificó
    if (formData.password) {
      updateData.password = formData.password
    }
    
    // Actualizar perfil
    const response = await usuarioService.updateProfile(authStore.user.id, updateData)
    
    // Actualizar el store con los nuevos datos
    const updatedUser = {
      ...authStore.user,
      nombre: response.data.nombre,
      email: response.data.email,
      telefono: response.data.telefono
    }
    authStore.user = updatedUser
    localStorage.setItem('user', JSON.stringify(updatedUser))
    
    success.value = 'Perfil actualizado correctamente'
    
    // Resetear formulario después de 2 segundos
    setTimeout(() => {
      showEditForm.value = false
      success.value = ''
      formData.password = ''
      formData.confirmPassword = ''
    }, 2000)
    
  } catch (err) {
    console.error('Error actualizando perfil:', err)
    
    // Manejar errores específicos
    if (err.response?.data) {
      const errorData = err.response.data
      
      // Error de email duplicado
      if (errorData.email) {
        error.value = 'Ya existe un usuario con ese correo electrónico'
      }
      // Error de contraseña igual a la anterior
      else if (errorData.password) {
        error.value = 'La nueva contraseña debe ser diferente a la anterior'
      }
      // Otros errores
      else if (errorData.detail || errorData.message) {
        error.value = errorData.detail || errorData.message
      }
      else {
        error.value = 'Error al actualizar el perfil'
      }
    } else {
      error.value = 'Error al actualizar el perfil. Inténtalo de nuevo.'
    }
  } finally {
    isSaving.value = false
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

.perfil-content {
  padding: 2rem;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

h1 {
  font-size: 42px;
  margin-bottom: 3rem;
  color: #fff;
  font-weight: 900;
  letter-spacing: -0.02em;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

h2 {
  font-size: 24px;
  margin-bottom: 2rem;
  color: #000;
  font-weight: 800;
  letter-spacing: -0.01em;
}

.perfil-card {
  background: #fff;
  padding: 3rem;
  border-radius: var(--radius-2xl, 20px);
  border: 2px solid var(--success, #00ff88);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  max-width: 800px;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

.loading {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 18px;
  font-weight: 600;
}

.info-section {
  margin-bottom: 3rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.info-item label {
  display: block;
  font-weight: 700;
  font-size: 12px;
  color: #666;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-item p {
  margin: 0;
  color: #000;
  font-size: 18px;
  font-weight: 700;
}

.actions {
  display: flex;
  gap: 1.5rem;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
}

.btn-secondary {
  padding: 1rem 2rem;
  background: #fff;
  color: #000;
  border: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.btn-secondary::before {
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

.btn-secondary:hover::before {
  width: 300px;
  height: 300px;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.edit-form {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
  animation: slideUp 0.3s ease;
}

.edit-form h2 {
  font-size: 20px;
  margin-bottom: 1.5rem;
  color: #000;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 12px;
  color: #666;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #000;
  background: #fff;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1);
}

.form-group input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
  opacity: 0.6;
}

.helper-text {
  display: block;
  margin-top: 0.5rem;
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.error-message {
  padding: 1rem;
  background: rgba(255, 68, 68, 0.1);
  border: 2px solid #ff4444;
  border-radius: 8px;
  color: #ff4444;
  font-weight: 700;
  margin-bottom: 1.5rem;
  animation: slideUp 0.3s ease;
}

.success-message {
  padding: 1rem;
  background: rgba(0, 255, 136, 0.1);
  border: 2px solid #00ff88;
  border-radius: 8px;
  color: #00ff88;
  font-weight: 700;
  margin-bottom: 1.5rem;
  animation: slideUp 0.3s ease;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary {
  padding: 1rem 2rem;
  background: #00ff88;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
}

.btn-primary:hover:not(:disabled) {
  background: #00dd77;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-cancel {
  padding: 1rem 2rem;
  background: transparent;
  color: #666;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel:hover {
  border-color: #666;
  color: #000;
  transform: translateY(-2px);
}

.info-message {
  color: var(--text-secondary, #a0a0a0);
  font-style: italic;
  font-weight: 500;
}
</style>
