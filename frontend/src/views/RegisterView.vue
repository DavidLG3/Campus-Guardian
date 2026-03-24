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
            placeholder="Juan Pérez García"
            maxlength="100"
            @blur="validateNombre"
            :class="{ 'input-error': validationErrors.nombre }"
          />
          <small v-if="validationErrors.nombre" class="error-text">{{ validationErrors.nombre }}</small>
          <small v-else class="help-text">Mínimo 2 caracteres, máximo 100</small>
        </div>
        
        <div class="form-group">
          <label for="email">Email institucional UAM</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            required
            placeholder="nombre.apellido@uam.es"
            maxlength="254"
            @blur="validateEmail"
            @input="validateEmail"
            :class="{ 'input-error': validationErrors.email }"
          />
          <small v-if="validationErrors.email" class="error-text">{{ validationErrors.email }}</small>
          <small v-else class="help-text">Solo correos @uam.es o @estudiante.uam.es</small>
        </div>
        
        <div class="form-group">
          <label for="telefono">Teléfono (opcional)</label>
          <div class="phone-input-group">
            <select 
              v-model="formData.prefijo" 
              class="phone-prefix"
              :class="{ 'input-error': validationErrors.telefono }"
            >
              <option value="+34">🇪🇸 +34</option>
              <option value="+1">🇺🇸 +1</option>
              <option value="+44">🇬🇧 +44</option>
              <option value="+33">🇫🇷 +33</option>
              <option value="+49">🇩🇪 +49</option>
              <option value="+39">🇮🇹 +39</option>
              <option value="+351">🇵🇹 +351</option>
              <option value="+52">🇲🇽 +52</option>
              <option value="+54">🇦🇷 +54</option>
              <option value="+56">🇨🇱 +56</option>
              <option value="+57">🇨🇴 +57</option>
            </select>
            <input
              id="telefono"
              v-model="formData.telefono"
              type="tel"
              placeholder="600000000"
              maxlength="9"
              @input="validateTelefono"
              @blur="validateTelefono"
              :class="{ 'input-error': validationErrors.telefono }"
            />
          </div>
          <small v-if="validationErrors.telefono" class="error-text">{{ validationErrors.telefono }}</small>
          <small v-else class="help-text">Opcional. Exactamente 9 dígitos</small>
        </div>
        
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            required
            minlength="8"
            maxlength="128"
            placeholder="••••••••"
            @input="validatePassword"
            @blur="validatePassword"
            :class="{ 'input-error': validationErrors.password }"
          />
          <div class="password-requirements">
            <small :class="{ 'req-met': passwordChecks.length, 'req-unmet': !passwordChecks.length }">
              ✓ Mínimo 8 caracteres
            </small>
            <small :class="{ 'req-met': passwordChecks.lowercase, 'req-unmet': !passwordChecks.lowercase }">
              ✓ Una letra minúscula
            </small>
            <small :class="{ 'req-met': passwordChecks.uppercase, 'req-unmet': !passwordChecks.uppercase }">
              ✓ Una letra mayúscula
            </small>
            <small :class="{ 'req-met': passwordChecks.number, 'req-unmet': !passwordChecks.number }">
              ✓ Un número
            </small>
            <small :class="{ 'req-met': passwordChecks.special, 'req-unmet': !passwordChecks.special }">
              ✓ Un carácter especial (!@#$%...)
            </small>
            <small :class="{ 'req-met': passwordChecks.noSpaces, 'req-unmet': !passwordChecks.noSpaces }">
              ✓ Sin espacios
            </small>
          </div>
          <small v-if="validationErrors.password" class="error-text">{{ validationErrors.password }}</small>
        </div>
        
        <div class="form-group">
          <label for="password2">Confirmar contraseña</label>
          <input
            id="password2"
            v-model="formData.password2"
            type="password"
            required
            placeholder="••••••••"
            @blur="validatePassword2"
            @input="validatePassword2"
            :class="{ 'input-error': validationErrors.password2 }"
          />
          <small v-if="validationErrors.password2" class="error-text">{{ validationErrors.password2 }}</small>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AvatarEditor from '@/components/AvatarEditor.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  nombre: '',
  email: '',
  prefijo: '+34',
  telefono: '',
  password: '',
  password2: ''
})

const validationErrors = ref({
  nombre: '',
  email: '',
  telefono: '',
  password: '',
  password2: ''
})

const passwordChecks = ref({
  length: false,
  lowercase: false,
  uppercase: false,
  number: false,
  special: false,
  noSpaces: false
})

const error = ref('')
const success = ref('')
const isLoading = ref(false)
const showAvatarEditor = ref(false)
const avatarPreview = ref(null)
const avatarBlob = ref(null)

function validateNombre() {
  const nombre = formData.value.nombre.trim()
  
  if (!nombre) {
    validationErrors.value.nombre = 'El nombre es requerido'
    return false
  }
  
  if (nombre.length < 2) {
    validationErrors.value.nombre = 'El nombre debe tener al menos 2 caracteres'
    return false
  }
  
  if (nombre.length > 100) {
    validationErrors.value.nombre = 'El nombre es demasiado largo (máximo 100 caracteres)'
    return false
  }
  
  if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-']+$/.test(nombre)) {
    validationErrors.value.nombre = 'El nombre solo puede contener letras, espacios, guiones y apóstrofes'
    return false
  }
  
  validationErrors.value.nombre = ''
  return true
}

function validateEmail() {
  const email = formData.value.email.trim().toLowerCase()
  
  if (!email) {
    validationErrors.value.email = 'El email es requerido'
    return false
  }
  
  // Validar que tenga exactamente un @
  const atCount = (email.match(/@/g) || []).length
  if (atCount !== 1) {
    validationErrors.value.email = 'El email debe contener exactamente un símbolo @'
    return false
  }
  
  // Validar dominio UAM
  if (!email.endsWith('@uam.es') && !email.endsWith('@estudiante.uam.es')) {
    validationErrors.value.email = 'Solo se permiten correos @uam.es o @estudiante.uam.es'
    return false
  }
  
  // Validar longitud
  if (email.length > 254) {
    validationErrors.value.email = 'El email es demasiado largo'
    return false
  }
  
  // Validar parte local
  const parteLocal = email.split('@')[0]
  if (!parteLocal || parteLocal.length < 1) {
    validationErrors.value.email = 'El email no es válido'
    return false
  }
  
  if (!/^[a-z0-9._-]+$/.test(parteLocal)) {
    validationErrors.value.email = 'El email solo puede contener letras, números, puntos, guiones y guiones bajos antes del @'
    return false
  }
  
  validationErrors.value.email = ''
  formData.value.email = email
  return true
}

function validateTelefono() {
  const telefono = formData.value.telefono.trim()
  
  if (!telefono) {
    validationErrors.value.telefono = ''
    return true
  }
  
  // Solo permitir dígitos
  if (!/^\d+$/.test(telefono)) {
    validationErrors.value.telefono = 'Solo se permiten números'
    return false
  }
  
  // Exactamente 9 dígitos
  if (telefono.length !== 9) {
    validationErrors.value.telefono = 'Debe tener exactamente 9 dígitos'
    return false
  }
  
  validationErrors.value.telefono = ''
  return true
}

function validatePassword() {
  const pwd = formData.value.password
  
  // Actualizar checks visuales
  passwordChecks.value.length = pwd.length >= 8 && pwd.length <= 128
  passwordChecks.value.lowercase = /[a-z]/.test(pwd)
  passwordChecks.value.uppercase = /[A-Z]/.test(pwd)
  passwordChecks.value.number = /\d/.test(pwd)
  passwordChecks.value.special = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]/.test(pwd)
  passwordChecks.value.noSpaces = !/\s/.test(pwd)
  
  if (!pwd) {
    validationErrors.value.password = 'La contraseña es requerida'
    return false
  }
  
  if (pwd.length < 8) {
    validationErrors.value.password = 'Mínimo 8 caracteres'
    return false
  }
  
  if (pwd.length > 128) {
    validationErrors.value.password = 'Máximo 128 caracteres'
    return false
  }
  
  if (!passwordChecks.value.lowercase) {
    validationErrors.value.password = 'Debe contener al menos una letra minúscula'
    return false
  }
  
  if (!passwordChecks.value.uppercase) {
    validationErrors.value.password = 'Debe contener al menos una letra mayúscula'
    return false
  }
  
  if (!passwordChecks.value.number) {
    validationErrors.value.password = 'Debe contener al menos un número'
    return false
  }
  
  if (!passwordChecks.value.special) {
    validationErrors.value.password = 'Debe contener al menos un carácter especial (!@#$%...)'
    return false
  }
  
  if (!passwordChecks.value.noSpaces) {
    validationErrors.value.password = 'No puede contener espacios'
    return false
  }
  
  validationErrors.value.password = ''
  return true
}

function validatePassword2() {
  if (!formData.value.password2) {
    validationErrors.value.password2 = 'Debes confirmar la contraseña'
    return false
  }
  
  if (formData.value.password !== formData.value.password2) {
    validationErrors.value.password2 = 'Las contraseñas no coinciden'
    return false
  }
  
  validationErrors.value.password2 = ''
  return true
}

function handleAvatarSave(blob) {
  avatarBlob.value = blob
  avatarPreview.value = URL.createObjectURL(blob)
  showAvatarEditor.value = false
}

async function handleRegister() {
  error.value = ''
  success.value = ''
  
  // Validar todos los campos
  const nombreValid = validateNombre()
  const emailValid = validateEmail()
  const telefonoValid = validateTelefono()
  const passwordValid = validatePassword()
  const password2Valid = validatePassword2()
  
  if (!nombreValid || !emailValid || !telefonoValid || !passwordValid || !password2Valid) {
    error.value = 'Por favor, corrige los errores en el formulario'
    return
  }
  
  isLoading.value = true
  
  try {
    // Combinar prefijo + teléfono si está presente
    const telefonoCompleto = formData.value.telefono 
      ? `${formData.value.prefijo}${formData.value.telefono}`
      : ''
    
    // Registrar usuario (siempre como ciudadano)
    await authStore.register({
      nombre: formData.value.nombre,
      email: formData.value.email,
      telefono: telefonoCompleto,
      rol: 'ciudadano',
      password: formData.value.password
    })
    
    success.value = 'Cuenta creada exitosamente. Iniciando sesión...'
    
    // Iniciar sesión automáticamente
    await authStore.login({
      email: formData.value.email,
      password: formData.value.password
    })
    
    // Si hay avatar, subirlo después del login
    if (avatarBlob.value && authStore.user) {
      try {
        const formDataAvatar = new FormData()
        formDataAvatar.append('foto_perfil', avatarBlob.value, 'avatar.jpg')
        
        const usuarioService = await import('@/services/usuarioService')
        await usuarioService.default.updateProfile(authStore.user.id, formDataAvatar)
      } catch (avatarErr) {
        console.error('Error al subir avatar:', avatarErr)
        // No bloqueamos el inicio de sesión por error en avatar
      }
    }
    
    // Redirigir según el tipo de usuario
    setTimeout(() => {
      if (authStore.user?.tipo === 'admin') {
        router.push('/admin')
      } else if (authStore.user?.tipo === 'seguridad') {
        router.push('/dashboard')
      } else {
        router.push('/dashboard')
      }
    }, 1500)
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

/* Validaciones en tiempo real */
.input-error {
  border-color: #ff4444 !important;
  background: rgba(255, 68, 68, 0.1);
}

.input-error:focus {
  border-color: #ff4444 !important;
  box-shadow: 0 0 0 3px rgba(255, 68, 68, 0.1);
}

.error-text {
  display: block;
  color: #ff4444;
  font-size: 12px;
  margin-top: 0.5rem;
  font-weight: 600;
  animation: shake 0.4s;
}

.password-requirements {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.password-requirements small {
  font-size: 11px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.req-met {
  color: #00ff88;
}

.req-unmet {
  color: #888;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

/* Grupo de input de teléfono */
.phone-input-group {
  display: flex;
  gap: 0.5rem;
}

.phone-prefix {
  flex: 0 0 120px;
  padding: 0.75rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
}

.phone-prefix:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(0, 255, 136, 0.3);
}

.phone-prefix:focus {
  outline: none;
  border-color: #00ff88;
  box-shadow: 0 0 0 3px rgba(0, 255, 136, 0.1);
}

.phone-prefix option {
  background: #1a1a1a;
  color: #fff;
}

.phone-input-group input {
  flex: 1;
}
</style>

