<template>
  <div class="perfil-view">
    <AppLayout>
      <div class="perfil-content">
        <div class="header-section">
          <div class="avatar-container">
            <div class="avatar">
              <img v-if="authStore.user?.foto_perfil_url" 
                   :src="authStore.user.foto_perfil_url" 
                   alt="Avatar" 
                   class="avatar-image" 
                   @click="showImagePreview = true"
                   style="cursor: pointer;" />
              <span v-else class="avatar-initial">{{ getInitials() }}</span>
              <div class="avatar-glow"></div>
              <button class="avatar-edit-btn" title="Editar foto" @click.stop="showAvatarEditor = true">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
                  <path d="M0 14.25V18h3.75L14.81 6.94l-3.75-3.75L0 14.25zM17.71 4.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </button>
            </div>
            <div class="user-header">
              <h1>{{ authStore.user?.nombre || 'Usuario' }}</h1>
              <div class="role-badge" :class="`role-${authStore.userRole}`">
                <span class="badge-icon">●</span>
                {{ formatRole(authStore.userRole) }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="perfil-card">
          <div v-if="isLoading" class="loading">
            <div class="loading-spinner"></div>
            <p>Cargando...</p>
          </div>
          
          <div v-else>
            <div class="info-section">
              <div class="section-header">
                <h2>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Información Personal
                </h2>
              </div>
              <div class="info-grid">
                <div class="info-item">
                  <div class="info-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                      <circle cx="12" cy="7" r="4"/>
                    </svg>
                  </div>
                  <div class="info-content">
                    <label>Nombre</label>
                    <p>{{ authStore.user?.nombre }}</p>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                      <polyline points="22,6 12,13 2,6"/>
                    </svg>
                  </div>
                  <div class="info-content">
                    <label>Email</label>
                    <p>{{ authStore.user?.email }}</p>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                    </svg>
                  </div>
                  <div class="info-content">
                    <label>Teléfono</label>
                    <p>{{ authStore.user?.telefono || 'No especificado' }}</p>
                  </div>
                </div>
                <div class="info-item">
                  <div class="info-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                      <circle cx="9" cy="7" r="4"/>
                      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                    </svg>
                  </div>
                  <div class="info-content">
                    <label>Rol</label>
                    <p>{{ formatRole(authStore.userRole) }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="actions">
              <button @click="toggleEditForm" class="btn-edit">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                </svg>
                {{ showEditForm ? 'Cancelar Edición' : 'Editar Perfil' }}
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
    
    <AvatarEditor 
      v-if="showAvatarEditor" 
      @close="showAvatarEditor = false"
      @save="handleAvatarSave"
    />
    
    <!-- Modal de vista previa de imagen -->
    <div v-if="showImagePreview" class="image-preview-modal" @click="showImagePreview = false">
      <div class="preview-content" @click.stop>
        <button @click="showImagePreview = false" class="preview-close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
        <img :src="authStore.user?.foto_perfil_url" alt="Foto de perfil" class="preview-image" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import usuarioService from '@/services/usuarioService'
import AppLayout from '@/layouts/AppLayout.vue'
import AvatarEditor from '@/components/AvatarEditor.vue'

const authStore = useAuthStore()
const isLoading = ref(false)
const showEditForm = ref(false)
const showAvatarEditor = ref(false)
const showImagePreview = ref(false)
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

function getInitials() {
  const nombre = authStore.user?.nombre || authStore.user?.username || 'U'
  return nombre.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatRole(role) {
  const roles = {
    'admin': 'Administrador',
    'operador': 'Operador',
    'ciudadano': 'Ciudadano'
  }
  return roles[role] || role
}

async function handleAvatarSave(blob) {
  try {
    const formData = new FormData()
    formData.append('foto_perfil', blob, 'avatar.jpg')
    
    const response = await usuarioService.updateProfile(authStore.user.id, formData)
    
    // Actualizar solo la foto de perfil, manteniendo todos los demás datos
    authStore.user.foto_perfil_url = response.data.foto_perfil_url
    
    // Actualizar localStorage con todos los datos
    localStorage.setItem('user', JSON.stringify(authStore.user))
    
    showAvatarEditor.value = false
  } catch (err) {
    console.error('Error al guardar avatar:', err)
    alert('Error al guardar la foto de perfil')
  }
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
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.perfil-content {
  padding: 2rem;
  animation: fadeIn 0.4s ease;
  background: #000;
  min-height: 100vh;
}

.header-section {
  margin-bottom: 3rem;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.avatar {
  position: relative;
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.4);
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
}

.avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 40px rgba(0, 255, 136, 0.5);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-initial {
  font-size: 48px;
  font-weight: 900;
  color: #000;
  letter-spacing: -0.02em;
}

.avatar-edit-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background: #00ff88;
  border: 3px solid #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  padding: 0;
}

.avatar-edit-btn:hover {
  background: #00dd77;
  transform: scale(1.1);
}

.avatar-edit-btn svg {
  width: 16px;
  height: 16px;
  fill: #000;
  flex-shrink: 0;
  position: relative;
  top: -2px;
  left: -2px;
}

.avatar-glow {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  border-radius: 50%;
  opacity: 0.3;
  filter: blur(20px);
  z-index: -1;
  animation: pulse 3s ease-in-out infinite;
}

.user-header h1 {
  font-size: 48px;
  margin: 0 0 0.75rem 0;
  color: #fff;
  font-weight: 900;
  letter-spacing: -0.02em;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}

.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 2px solid;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
}

.role-badge.role-admin {
  color: #ff4444;
  border-color: #ff4444;
  box-shadow: 0 0 20px rgba(255, 68, 68, 0.3);
}

.role-badge.role-operador {
  color: #ffcc00;
  border-color: #ffcc00;
  box-shadow: 0 0 20px rgba(255, 204, 0, 0.3);
}

.role-badge.role-ciudadano {
  color: #00ccff;
  border-color: #00ccff;
  box-shadow: 0 0 20px rgba(0, 204, 255, 0.3);
}

.badge-icon {
  font-size: 20px;
  animation: pulse 2s ease-in-out infinite;
}

.perfil-card {
  background: #fff;
  padding: 3rem;
  border-radius: 24px;
  border: 2px solid #00ff88;
  box-shadow: 0 8px 32px rgba(0, 255, 136, 0.2);
  max-width: 1000px;
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
}

.loading {
  text-align: center;
  padding: 4rem;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f0f0f0;
  border-top: 4px solid #00ff88;
  border-radius: 50%;
  margin: 0 auto 1.5rem;
  animation: rotate 1s linear infinite;
}

.loading p {
  color: #666;
  font-size: 18px;
  font-weight: 600;
}

.info-section {
  margin-bottom: 3rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 24px;
  color: #000;
  font-weight: 900;
  letter-spacing: -0.01em;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-header svg {
  color: #00ff88;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.info-item {
  display: flex;
  gap: 1.25rem;
  padding: 1.5rem;
  background: #f8f8f8;
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.info-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #00ff88, #00ccff);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.info-item:hover {
  border-color: #00ff88;
  background: #fff;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.15);
  transform: translateY(-2px);
}

.info-item:hover::before {
  transform: scaleX(1);
}

.info-icon {
  width: 48px;
  height: 48px;
  min-width: 48px;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
}

.info-icon svg {
  color: #000;
}

.info-content {
  flex: 1;
}

.info-content label {
  display: block;
  font-weight: 700;
  font-size: 11px;
  color: #666;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.info-content p {
  margin: 0;
  color: #000;
  font-size: 18px;
  font-weight: 700;
  word-break: break-word;
}

.actions {
  display: flex;
  gap: 1.5rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
}

.btn-edit {
  padding: 1rem 2.5rem;
  background: linear-gradient(135deg, #00ff88, #00dd77);
  color: #000;
  border: none;
  border-radius: 12px;
  font-weight: 900;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.3);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-edit:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.5);
}

.btn-edit svg {
  transition: transform 0.3s ease;
}

.btn-edit:hover svg {
  transform: rotate(15deg);
}

.edit-form {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #f0f0f0;
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

/* Modal de vista previa de imagen */
.image-preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

.preview-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-image {
  max-width: 100%;
  max-height: 90vh;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 255, 136, 0.3);
  border: 3px solid #00ff88;
}

.preview-close-btn {
  position: absolute;
  top: -50px;
  right: 0;
  background: #00ff88;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.4);
  padding: 0;
}

.preview-close-btn:hover {
  background: #00dd77;
  transform: scale(1.1);
}

.preview-close-btn svg {
  width: 20px;
  height: 20px;
  fill: #000;
}

/* Responsive */
@media (max-width: 768px) {
  .perfil-content {
    padding: 1.5rem;
  }

  .avatar-container {
    flex-direction: column;
    text-align: center;
  }

  .avatar {
    width: 100px;
    height: 100px;
  }

  .avatar-initial {
    font-size: 40px;
  }

  .user-header h1 {
    font-size: 36px;
  }

  .perfil-card {
    padding: 2rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .actions {
    flex-direction: column;
  }

  .btn-edit {
    width: 100%;
    justify-content: center;
  }

  .form-actions {
    flex-direction: column;
  }
  
  .preview-close-btn {
    top: 10px;
    right: 10px;
  }
}
</style>
