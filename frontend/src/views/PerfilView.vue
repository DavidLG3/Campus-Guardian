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
              <button @click="showEditForm = !showEditForm" class="btn-secondary">
                {{ showEditForm ? 'Cancelar' : 'Editar Perfil' }}
              </button>
            </div>
            
            <div v-if="showEditForm" class="edit-form">
              <h2>Editar Información</h2>
              <p class="info-message">Funcionalidad próximamente</p>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const isLoading = ref(false)
const showEditForm = ref(false)

function formatRole(role) {
  const roles = {
    'admin': 'Administrador',
    'operador': 'Operador',
    'ciudadano': 'Ciudadano'
  }
  return roles[role] || role
}
</script>

<style scoped>
.perfil-content {
  padding: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #444;
}

.perfil-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 800px;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.info-section {
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-item label {
  display: block;
  font-weight: 600;
  color: #666;
  margin-bottom: 0.5rem;
}

.info-item p {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-secondary:hover {
  opacity: 0.9;
}

.edit-form {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.info-message {
  color: #666;
  font-style: italic;
}
</style>
