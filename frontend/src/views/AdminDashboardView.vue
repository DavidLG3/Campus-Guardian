<template>
  <AppLayout>
    <div class="admin-dashboard">
      <h1>Panel de Administración</h1>
      
      <!-- Accesos Rápidos -->
      <section class="acciones-rapidas">
        <h2>Accesos Rápidos</h2>
        <div class="actions-grid">
          <router-link to="/admin/usuarios" class="action-card">
            <div class="action-icon">👥</div>
            <span>Gestionar Usuarios</span>
          </router-link>
          
          <router-link to="/incidencias" class="action-card">
            <div class="action-icon">📋</div>
            <span>Ver Incidencias</span>
          </router-link>
          
          <router-link to="/mapa" class="action-card">
            <div class="action-icon">🗺️</div>
            <span>Ver Mapas</span>
          </router-link>
          
          <router-link to="/admin/crear-seguridad" class="action-card">
            <div class="action-icon">➕</div>
            <span>Crear Usuario Seguridad</span>
          </router-link>
        </div>
      </section>

      <!-- Estadísticas Generales -->
      <section class="estadisticas">
        <h2>Estadísticas del Sistema</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">👤</div>
            <div class="stat-info">
              <h3>{{ estadisticas.usuariosNormales }}</h3>
              <p>Usuarios Normales</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🛡️</div>
            <div class="stat-info">
              <h3>{{ estadisticas.usuariosSeguridad }}</h3>
              <p>Personal de Seguridad</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3>{{ estadisticas.incidenciasActivas }}</h3>
              <p>Incidencias Activas</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-info">
              <h3>{{ estadisticas.incidenciasResueltas }}</h3>
              <p>Incidencias Resueltas</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useIncidenciaStore } from '@/stores/incidencia'
import adminService from '@/services/adminService'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const incidenciaStore = useIncidenciaStore()

const usuarios = ref([])
const isLoading = ref(false)

const estadisticas = computed(() => {
  const usuariosNormales = usuarios.value.filter(u => u.tipo === 'normal').length
  const usuariosSeguridad = usuarios.value.filter(u => u.tipo === 'seguridad').length
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  const incidenciasActivas = incidencias.filter(i => i.estado !== 'resuelta').length
  const incidenciasResueltas = incidencias.filter(i => i.estado === 'resuelta').length
  
  return {
    usuariosNormales,
    usuariosSeguridad,
    incidenciasActivas,
    incidenciasResueltas
  }
})

onMounted(async () => {
  isLoading.value = true
  try {
    // Cargar usuarios
    const response = await adminService.listarUsuarios()
    usuarios.value = response.data
    
    // Cargar incidencias
    await incidenciaStore.fetchAll()
  } catch (error) {
    console.error('Error cargando datos:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
  background: #000;
  min-height: 100vh;
  color: #fff;
}

h1 {
  font-size: 42px;
  margin-bottom: 2rem;
  font-weight: 900;
  letter-spacing: -0.02em;
}

h2 {
  font-size: 24px;
  margin-bottom: 1.5rem;
  font-weight: 700;
  color: #00ff88;
}

.acciones-rapidas {
  margin-bottom: 3rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: #111;
  border: 2px solid #222;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  text-decoration: none;
  color: #fff;
  transition: all 0.3s;
  cursor: pointer;
}

.action-card:hover {
  border-color: #00ff88;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.2);
}

.action-icon {
  font-size: 48px;
  margin-bottom: 1rem;
}

.action-card span {
  font-size: 18px;
  font-weight: 700;
  display: block;
}

.estadisticas {
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: #111;
  border: 2px solid #222;
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: #00ff88;
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 48px;
}

.stat-info h3 {
  font-size: 36px;
  font-weight: 900;
  color: #00ff88;
  margin: 0;
}

.stat-info p {
  font-size: 14px;
  color: #999;
  margin: 0;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  h1 {
    font-size: 32px;
  }

  .actions-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
