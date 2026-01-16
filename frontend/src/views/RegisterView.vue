<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Campus Guardian</h1>
      <h2>Crear Cuenta</h2>
      
      <div class="avatar-section">
        <div class="avatar-preview" @click="showAvatarEditor = true">
          <img v-if="avatarPreview" :src="avatarPreview" alt="Avatar" class="avatar-image" />
          <div v-else class="avatar-placeholder">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
          </div>
          <button type="button" class="avatar-edit-btn" title="Añadir foto">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5v14M5 12h14"/>
            </svg>
          </button>
        </div>
        <p class="avatar-label">Foto de perfil (opcional)</p>
      </div>
      
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
            pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            title="Introduce un email válido (ejemplo@dominio.com)"
          />
        </div>
        
        <div class="form-group">
          <label for="telefono">Teléfono (opcional)</label>
          <input
            id="telefono"
            v-model="formData.telefono"
            type="tel"
            placeholder="+34 600 000 000"
            pattern="[\+]?[0-9\s\-\(\)]{9,20}"
            title="Introduce un número de teléfono válido (9-15 dígitos)"
          />
          <small class="help-text">Opcional. Puedes incluir código de país (+34, +1, etc.)</small>
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
            minlength="6"
            placeholder="••••••••"
            title="Mínimo 6 caracteres, debe incluir letras y números"
          />
          <small class="help-text">Mínimo 6 caracteres, debe contener letras y números</small>
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
          <span>{{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}</span>
        </button>
      </form>
      
      <p class="login-link">
        ¿Ya tienes cuenta? 
        <router-link to="/login">Inicia sesión aquí</router-link>
      </p>
    </div>
    
    <AvatarEditor 
      v-if="showAvatarEditor" 
      @close="showAvatarEditor = false"
      @save="handleAvatarSave"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AvatarEditor from '@/components/AvatarEditor.vue'

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
const showAvatarEditor = ref(false)
const avatarPreview = ref(null)
const avatarBlob = ref(null)

function handleAvatarSave(blob) {
  avatarBlob.value = blob
  avatarPreview.value = URL.createObjectURL(blob)
  showAvatarEditor.value = false
}

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
    // Registrar usuario
    await authStore.register({
      nombre: formData.value.nombre,
      email: formData.value.email,
      telefono: formData.value.telefono,
      rol: formData.value.rol,
      password: formData.value.password
    })
    
    // Si hay avatar, subirlo después del registro
    if (avatarBlob.value && authStore.user) {
      try {
        const formDataAvatar = new FormData()
        formDataAvatar.append('foto_perfil', avatarBlob.value, 'avatar.jpg')
        
        const usuarioService = await import('@/services/usuarioService')
        await usuarioService.default.updateProfile(authStore.user.id, formDataAvatar)
      } catch (avatarErr) {
        console.error('Error al subir avatar:', avatarErr)
        // No bloqueamos el registro por error en avatar
      }
    }
    
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

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #000;
  padding: 2rem 1rem;
  position: relative;
  overflow: hidden;
}

.register-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(255, 204, 0, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 7s ease-in-out infinite;
  pointer-events: none;
}

.register-container::after {
  content: '';
  position: absolute;
  bottom: -30%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 204, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: float 9s ease-in-out infinite reverse;
  pointer-events: none;
}

.register-card {
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

.register-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-2xl, 20px);
  padding: 2px;
  background: linear-gradient(135deg, rgba(255, 204, 0, 0.3), rgba(0, 204, 255, 0.3));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}

.register-card:hover::before {
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
  margin-bottom: 2rem;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.01em;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s backwards;
}

.avatar-section {
  text-align: center;
  margin-bottom: 2rem;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.3s backwards;
}

.avatar-preview {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

.avatar-preview:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 32px rgba(0, 255, 136, 0.4);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-placeholder {
  color: #000;
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
}

.avatar-edit-btn:hover {
  background: #00dd77;
  transform: scale(1.1);
}

.avatar-edit-btn svg {
  color: #000;
}

.avatar-label {
  margin: 0;
  font-size: 14px;
  color: #a0a0a0;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.25rem;
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) calc(0.3s + var(--delay, 0s)) backwards;
}

.form-group:nth-child(1) {
  --delay: 0s;
}

.form-group:nth-child(2) {
  --delay: 0.05s;
}

.form-group:nth-child(3) {
  --delay: 0.1s;
}

.form-group:nth-child(4) {
  --delay: 0.15s;
}

.form-group:nth-child(5) {
  --delay: 0.2s;
}

.form-group:nth-child(6) {
  --delay: 0.25s;
}

label {
  display: block;
  margin-bottom: 0.75rem;
  color: #fff;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

input,
select {
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

select option {
  background: #1a1a1a;
  color: #fff;
}

input:focus,
select:focus {
  outline: none;
  border-color: var(--warning, #ffcc00);
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 204, 0, 0.2);
}

.help-text {
  display: block;
  margin-top: 0.75rem;
  font-size: 12px;
  color: var(--text-secondary, #a0a0a0);
  line-height: 1.6;
  font-weight: 500;
  background: rgba(255, 204, 0, 0.05);
  padding: 0.75rem;
  border-radius: var(--radius-md, 8px);
  border-left: 3px solid var(--warning, #ffcc00);
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

.success-message {
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(0, 255, 136, 0.1) 100%);
  color: var(--success, #00ff88);
  padding: 1rem 1.25rem;
  border-radius: var(--radius-lg, 12px);
  border: 2px solid rgba(0, 255, 136, 0.3);
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
  animation: slideUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.5s backwards;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--warning, #ffcc00);
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

.login-link {
  text-align: center;
  margin-top: 2rem;
  color: var(--text-secondary, #a0a0a0);
  font-size: 14px;
  font-weight: 600;
  animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.6s backwards;
}

.login-link a {
  color: var(--warning, #ffcc00);
  text-decoration: none;
  font-weight: 800;
  letter-spacing: 0.02em;
  transition: all var(--transition-fast, 0.15s);
  position: relative;
}

.login-link a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--warning, #ffcc00);
  transition: width var(--transition-base, 0.3s);
}

.login-link a:hover {
  color: #fff;
}

.login-link a:hover::after {
  width: 100%;
}
</style>
