<template>
  <AppLayout>
    <div class="usuarios-admin">
      <div class="header">
        <h1>Gestión de Usuarios</h1>
        <router-link to="/admin/crear-seguridad" class="btn-primary">
          ➕ Crear Usuario de Seguridad
        </router-link>
      </div>

      <!-- Buscador y Filtros -->
      <div class="search-filters">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre, email o usuario..."
          class="search-input"
        />
        <select v-model="filtroTipo" class="filter-select">
          <option value="">Todos los tipos</option>
          <option value="normal">Miembros</option>
          <option value="seguridad">Personal de Seguridad</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="loading">Cargando usuarios...</div>

      <!-- Mensaje de error -->
      <div v-else-if="error" class="error">{{ error }}</div>

      <!-- Lista de Usuarios -->
      <div v-else class="usuarios-container">
        <!-- Miembros -->
        <section v-if="usuariosNormalesFiltrados.length > 0" class="usuarios-section">
          <h2>👤 Miembros ({{ usuariosNormalesFiltrados.length }})</h2>
          <div class="usuarios-grid">
            <div
              v-for="usuario in usuariosNormalesFiltrados"
              :key="usuario.id"
              class="usuario-card"
            >
              <div class="usuario-info">
                <div class="usuario-avatar">
                  <img v-if="usuario.foto_perfil" :src="usuario.foto_perfil" alt="Avatar" />
                  <span v-else class="avatar-placeholder">{{ getInitials(usuario) }}</span>
                </div>
                <div class="usuario-detalles">
                  <h3>{{ usuario.first_name }} {{ usuario.last_name }}</h3>
                  <p class="email">{{ usuario.email }}</p>
                  <p class="username">@{{ usuario.username }}</p>
                  <p v-if="usuario.telefono" class="telefono">📞 {{ usuario.telefono }}</p>
                </div>
              </div>
              <div class="usuario-actions">
                <button @click="eliminarUsuario(usuario)" class="btn-eliminar">
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Usuarios de Seguridad -->
        <section v-if="usuariosSeguridadFiltrados.length > 0" class="usuarios-section">
          <h2>🛡️ Personal de Seguridad ({{ usuariosSeguridadFiltrados.length }})</h2>
          <div class="usuarios-grid">
            <div
              v-for="usuario in usuariosSeguridadFiltrados"
              :key="usuario.id"
              class="usuario-card seguridad"
            >
              <div class="usuario-info">
                <div class="usuario-avatar">
                  <img v-if="usuario.foto_perfil" :src="usuario.foto_perfil" alt="Avatar" />
                  <span v-else class="avatar-placeholder">{{ getInitials(usuario) }}</span>
                </div>
                <div class="usuario-detalles">
                  <h3>{{ usuario.first_name }} {{ usuario.last_name }}</h3>
                  <p class="email">{{ usuario.email }}</p>
                  <p class="username">@{{ usuario.username }}</p>
                  <p v-if="usuario.telefono" class="telefono">📞 {{ usuario.telefono }}</p>
                </div>
              </div>
              <div class="usuario-actions">
                <button @click="eliminarUsuario(usuario)" class="btn-eliminar">
                  🗑️ Eliminar
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Sin resultados -->
        <div v-if="usuariosFiltrados.length === 0" class="empty">
          No se encontraron usuarios
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import adminService from '@/services/adminService'
import AppLayout from '@/layouts/AppLayout.vue'

const router = useRouter()

const usuarios = ref([])
const searchQuery = ref('')
const filtroTipo = ref('')
const isLoading = ref(false)
const error = ref(null)

// Computed
const usuariosFiltrados = computed(() => {
  let filtered = usuarios.value

  // Filtrar por tipo
  if (filtroTipo.value) {
    filtered = filtered.filter(u => u.tipo === filtroTipo.value)
  }

  // Filtrar por búsqueda (local, ya que el backend también filtra)
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(u => 
      u.first_name.toLowerCase().includes(query) ||
      u.last_name.toLowerCase().includes(query) ||
      u.email.toLowerCase().includes(query) ||
      u.username.toLowerCase().includes(query)
    )
  }

  return filtered
})

const usuariosNormalesFiltrados = computed(() => 
  usuariosFiltrados.value.filter(u => u.tipo === 'normal')
)

const usuariosSeguridadFiltrados = computed(() => 
  usuariosFiltrados.value.filter(u => u.tipo === 'seguridad')
)

// Métodos
function getInitials(usuario) {
  const first = usuario.first_name?.charAt(0) || ''
  const last = usuario.last_name?.charAt(0) || ''
  return (first + last).toUpperCase() || '??'
}

async function cargarUsuarios() {
  isLoading.value = true
  error.value = null
  try {
    const response = await adminService.listarUsuarios(filtroTipo.value, searchQuery.value)
    usuarios.value = response.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Error al cargar usuarios'
    console.error('Error cargando usuarios:', err)
  } finally {
    isLoading.value = false
  }
}

async function eliminarUsuario(usuario) {
  if (!confirm(`¿Estás seguro de que quieres eliminar a ${usuario.first_name} ${usuario.last_name}?`)) {
    return
  }

  try {
    await adminService.eliminarUsuario(usuario.id)
    usuarios.value = usuarios.value.filter(u => u.id !== usuario.id)
  } catch (err) {
    alert(err.response?.data?.message || 'Error al eliminar usuario')
    console.error('Error eliminando usuario:', err)
  }
}

// Watch para recargar cuando cambie el filtro
watch([filtroTipo], () => {
  cargarUsuarios()
})

// Montar componente
onMounted(() => {
  cargarUsuarios()
})
</script>

<style scoped>
.usuarios-admin {
  padding: 2rem;
  background: #000;
  min-height: 100vh;
  color: #fff;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 42px;
  font-weight: 900;
  letter-spacing: -0.02em;
  margin: 0;
}

.btn-primary {
  background: #00ff88;
  color: #000;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.3s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.3);
}

.search-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  background: #111;
  border: 2px solid #222;
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  transition: all 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #00ff88;
}

.filter-select {
  padding: 1rem 1.5rem;
  background: #111;
  border: 2px solid #222;
  border-radius: 12px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-select:hover,
.filter-select:focus {
  border-color: #00ff88;
  outline: none;
}

.loading,
.error,
.empty {
  text-align: center;
  padding: 3rem;
  font-size: 18px;
  color: #999;
}

.error {
  color: #ff4444;
}

.usuarios-section {
  margin-bottom: 3rem;
}

.usuarios-section h2 {
  font-size: 24px;
  margin-bottom: 1.5rem;
  font-weight: 700;
  color: #00ff88;
}

.usuarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.usuario-card {
  background: #111;
  border: 2px solid #222;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.usuario-card.seguridad {
  border-color: #00ccff;
}

.usuario-card:hover {
  border-color: #00ff88;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.2);
}

.usuario-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.usuario-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  background: #222;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.usuario-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 20px;
  font-weight: 700;
  color: #00ff88;
}

.usuario-detalles h3 {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #fff;
}

.usuario-detalles p {
  margin: 0.25rem 0;
  font-size: 14px;
  color: #999;
}

.usuario-detalles .email {
  color: #00ff88;
}

.usuario-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-eliminar {
  background: #ff4444;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-eliminar:hover {
  background: #cc0000;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .usuarios-admin {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .search-filters {
    flex-direction: column;
  }

  .usuarios-grid {
    grid-template-columns: 1fr;
  }
}
</style>
