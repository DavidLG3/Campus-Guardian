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
.nueva-alerta-content {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

textarea {
  resize: vertical;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success-message {
  background-color: #efe;
  color: #3c3;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-cancel:hover {
  opacity: 0.9;
}

.btn-submit {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-submit:hover {
  opacity: 0.9;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
