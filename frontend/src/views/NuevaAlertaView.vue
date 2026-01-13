<template>
  <div class="nueva-alerta-view">
    <AppLayout>
      <div class="nueva-alerta-content">
        <h1>Crear Nueva Alerta</h1>
        
        <div class="form-container">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="tipo">Tipo de Alerta *</label>
              <select id="tipo" v-model="formData.tipo" required>
                <option value="">Selecciona un tipo</option>
                <option value="emergencia">Emergencia</option>
                <option value="precaución">Precaución</option>
                <option value="información">Información</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="nivel">Nivel de Severidad *</label>
              <select id="nivel" v-model="formData.nivel" required>
                <option value="">Selecciona un nivel</option>
                <option value="bajo">Bajo</option>
                <option value="medio">Medio</option>
                <option value="alto">Alto</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="mensaje">Mensaje *</label>
              <textarea
                id="mensaje"
                v-model="formData.mensaje"
                required
                rows="4"
                placeholder="Describe la alerta con claridad..."
              ></textarea>
            </div>
            
            <div class="form-group">
              <label for="ubicacion">Ubicación Afectada</label>
              <input
                id="ubicacion"
                v-model="formData.ubicacion"
                type="text"
                placeholder="Zona, calle, barrio..."
              />
            </div>
            
            <div class="form-group">
              <label class="checkbox-label">
                <input
                  v-model="formData.activa"
                  type="checkbox"
                />
                <span>Activar alerta inmediatamente</span>
              </label>
            </div>
            
            <div v-if="error" class="error-message">
              {{ error }}
            </div>
            
            <div v-if="success" class="success-message">
              {{ success }}
            </div>
            
            <div class="form-actions">
              <router-link to="/alertas" class="btn-cancel">
                Cancelar
              </router-link>
              <button type="submit" :disabled="isLoading" class="btn-submit">
                {{ isLoading ? 'Creando...' : 'Crear Alerta' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAlertaStore } from '@/stores/alerta'
import AppLayout from '@/layouts/AppLayout.vue'

const router = useRouter()
const alertaStore = useAlertaStore()

const formData = ref({
  tipo: '',
  nivel: '',
  mensaje: '',
  ubicacion: '',
  activa: true
})

const isLoading = ref(false)
const error = ref('')
const success = ref('')

async function handleSubmit() {
  error.value = ''
  success.value = ''
  isLoading.value = true
  
  try {
    const data = {
      tipo: formData.value.tipo,
      nivel: formData.value.nivel,
      mensaje: formData.value.mensaje,
      activa: formData.value.activa
    }
    
    if (formData.value.ubicacion) {
      data.ubicacion = formData.value.ubicacion
    }
    
    await alertaStore.create(data)
    
    success.value = 'Alerta creada exitosamente. Redirigiendo...'
    
    setTimeout(() => {
      router.push('/alertas')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al crear la alerta'
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

.nueva-alerta-content {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
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

.form-container {
  background: #fff;
  border: 2px solid var(--success, #00ff88);
  border-radius: var(--radius-xl, 16px);
  padding: 2.5rem;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.2);
  animation: slideUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) 0.1s backwards;
}

.form-group {
  margin-bottom: 2rem;
}

label {
  display: block;
  margin-bottom: 0.75rem;
  color: #000;
  font-weight: 700;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

input,
textarea,
select {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid #e0e0e0;
  border-radius: var(--radius-lg, 12px);
  font-size: 14px;
  font-weight: 500;
  color: #000;
  background: #fff;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
}

select option {
  background: #1a1a1a;
  color: #fff;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: var(--info, #00ccff);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 16px rgba(0, 204, 255, 0.2);
  transform: translateY(-2px);
}

textarea {
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  color: #000;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--info, #00ccff);
}

.error-message {
  background: rgba(255, 68, 68, 0.1);
  color: var(--error, #ff4444);
  padding: 1rem;
  border-radius: var(--radius-lg, 12px);
  margin-bottom: 1.5rem;
  font-weight: 600;
  font-size: 14px;
  border: 2px solid rgba(255, 68, 68, 0.3);
  animation: slideUp 0.3s ease;
}

.success-message {
  background: rgba(0, 255, 136, 0.1);
  color: var(--success, #00ff88);
  padding: 1rem;
  border-radius: var(--radius-lg, 12px);
  margin-bottom: 1.5rem;
  font-weight: 600;
  font-size: 14px;
  border: 2px solid rgba(0, 255, 136, 0.3);
  animation: slideUp 0.3s ease;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2.5rem;
}

.btn-cancel {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  text-decoration: none;
  border-radius: var(--radius-lg, 12px);
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  transition: all var(--transition-base, 0.3s) cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.2);
}

.btn-submit {
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

.btn-submit::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: var(--info, #00ccff);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  z-index: 0;
}

.btn-submit:hover::before {
  width: 300px;
  height: 300px;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(255, 255, 255, 0.3);
  color: #666;
}

.btn-submit:disabled::before {
  display: none;
}

@media (max-width: 768px) {
  .nueva-alerta-content {
    padding: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .form-container {
    padding: 2rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .nueva-alerta-content {
    padding: 0.75rem;
  }

  h1 {
    font-size: 28px;
  }

  .form-container {
    padding: 1.5rem;
  }
}
</style>

