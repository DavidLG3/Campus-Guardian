<template>
  <div class="dashboard-view">
    <AppLayout>
      <div class="dashboard-content">
        <h1>Dashboard</h1>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
              <h3>{{ stats.incidencias }}</h3>
              <p>Incidencias Totales</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">⚠️</div>
            <div class="stat-info">
              <h3>{{ stats.incidenciasAbiertas }}</h3>
              <p>Incidencias Abiertas</p>
            </div>
          </div>
          
          <!-- Alertas: solo visible para admin y operador -->
          <div v-if="authStore.isAdmin || authStore.isOperador" class="stat-card">
            <div class="stat-icon">🔔</div>
            <div class="stat-info">
              <h3>{{ stats.alertasActivas }}</h3>
              <p>Alertas Activas</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-info">
              <h3>{{ stats.incidenciasResueltas }}</h3>
              <p>Incidencias Resueltas</p>
            </div>
          </div>
        </div>
        
        <div class="dashboard-sections">
          <div class="section">
            <h2>Incidencias Recientes</h2>
            <div v-if="isLoading" class="loading">Cargando...</div>
            <div v-else-if="incidenciasRecientes.length === 0" class="empty">
              No hay incidencias recientes
            </div>
            <div v-else class="incidencias-grid">
              <div 
                v-for="incidencia in incidenciasRecientes" 
                :key="incidencia.id"
                class="incidencia-card"
                @click="$router.push(`/incidencias/${incidencia.id}`)"
              >
                <div class="card-header">
                  <span class="codigo-badge">{{ incidencia.codigo_unico }}</span>
                  <span :class="['estado-badge', incidencia.estado]">{{ formatEstado(incidencia.estado) }}</span>
                </div>
                <div class="card-body">
                  <div class="tipo-incidencia">{{ formatTipo(incidencia.tipo) }}</div>
                  <p class="descripcion">{{ truncateText(incidencia.descripcion, 60) }}</p>
                </div>
                <div class="card-footer">
                  <span class="fecha">📅 {{ formatDate(incidencia.fecha_creacion) }}</span>
                  <span class="ubicacion" v-if="incidencia.ubicacion">📍 {{ incidencia.ubicacion }}</span>
                </div>
              </div>
            </div>
            <router-link to="/incidencias" class="view-all">Ver todas →</router-link>
          </div>
          
          <!-- Alertas Activas: solo visible para admin y operador -->
          <div v-if="authStore.isAdmin || authStore.isOperador" class="section">
            <h2>Alertas Activas</h2>
            <div v-if="isLoading" class="loading">Cargando...</div>
            <div v-else-if="alertasActivas.length === 0" class="empty">
              No hay alertas activas
            </div>
            <ul v-else class="alertas-list">
              <li v-for="alerta in alertasActivas" :key="alerta.id">
                <div :class="['alerta-item', alerta.nivel]">
                  <strong>{{ alerta.tipo }}</strong>
                  <p>{{ alerta.mensaje }}</p>
                  <span class="fecha">{{ formatDate(alerta.fecha_creacion) }}</span>
                </div>
              </li>
            </ul>
            <router-link to="/alertas" class="view-all">Ver todas →</router-link>
          </div>
        </div>
        
        <div class="quick-actions">
          <h2>Acciones Rápidas</h2>
          <div class="actions-grid">
            <router-link to="/incidencias/nueva" class="action-btn">
              ➕ Nueva Incidencia
            </router-link>
            <router-link to="/mapa" class="action-btn">
              🗺️ Ver Mapa
            </router-link>
            <router-link v-if="authStore.isCiudadano" to="/mis-incidencias" class="action-btn">
              📋 Mis Incidencias
            </router-link>
            <router-link v-if="authStore.isAdmin || authStore.isOperador" to="/alertas" class="action-btn">
              🔔 Ver Notificaciones
            </router-link>
          </div>
        </div>
      </div>
    </AppLayout>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useIncidenciaStore } from '@/stores/incidencia'
import { useAlertaStore } from '@/stores/alerta'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const incidenciaStore = useIncidenciaStore()
const alertaStore = useAlertaStore()

const isLoading = ref(false)

const stats = computed(() => {
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  const alertasActivasArray = Array.isArray(alertaStore.alertasActivas) ? alertaStore.alertasActivas : []
  
  return {
    incidencias: incidencias.length,
    incidenciasAbiertas: incidencias.filter(i => i.estado === 'abierta').length,
    incidenciasResueltas: incidencias.filter(i => i.estado === 'resuelta').length,
    alertasActivas: alertasActivasArray.length
  }
})

const incidenciasRecientes = computed(() => {
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  return incidencias.slice(0, 5)
})

const alertasActivas = computed(() => {
  const alertas = Array.isArray(alertaStore.alertasActivas) ? alertaStore.alertasActivas : []
  return alertas.slice(0, 5)
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatEstado(estado) {
  const estados = {
    'abierta': 'Abierta',
    'en_progreso': 'En Progreso',
    'resuelta': 'Resuelta',
    'pendiente': 'Pendiente'
  }
  return estados[estado] || estado
}

function formatTipo(tipo) {
  const tipos = {
    'robo': 'Robo',
    'vandalismo': 'Vandalismo',
    'accidente': 'Accidente',
    'otros': 'Otros'
  }
  return tipos[tipo] || tipo
}

function truncateText(text, maxLength) {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

onMounted(async () => {
  isLoading.value = true
  try {
    await Promise.all([
      incidenciaStore.fetchAll().catch(err => {
        console.error('Error cargando incidencias:', err)
        return []
      }),
      alertaStore.fetchAll().catch(err => {
        console.error('Error cargando alertas:', err)
        return []
      })
    ])
  } catch (error) {
    console.error('Error cargando datos del dashboard:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.dashboard-content {
  padding: 1rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

h2 {
  font-size: 1.2rem;
  margin-bottom: 0.75rem;
  color: #444;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  width: 100%;
  max-width: 100%;
}

.stat-card {
  background: white;
  padding: 0.75rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 0;
  overflow: hidden;
}

.stat-icon {
  font-size: 1.5rem;
}

.stat-info {
  min-width: 0;
  overflow: hidden;
}

.stat-info h3 {
  font-size: 1.5rem;
  margin: 0;
  color: #667eea;
}

.stat-info p {
  margin: 0;
  color: #666;
  font-size: 0.75rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dashboard-sections {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
  width: 100%;
  max-width: 100%;
}

.section {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.loading, .empty {
  text-align: center;
  padding: 1.5rem;
  color: #999;
  font-size: 0.9rem;
}

.incidencias-grid {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  width: 100%;
  max-width: 100%;
}

.incidencia-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.incidencia-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.codigo-badge {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.estado-badge {
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.65rem;
  font-weight: 600;
}

.estado-badge.abierta {
  background-color: #fff3cd;
  color: #856404;
}

.estado-badge.en_progreso {
  background-color: #cfe2ff;
  color: #084298;
}

.estado-badge.resuelta {
  background-color: #d1e7dd;
  color: #0f5132;
}

.card-body {
  margin-bottom: 0.5rem;
}

.tipo-incidencia {
  font-weight: 600;
  color: #333;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.descripcion {
  color: #666;
  font-size: 0.75rem;
  margin: 0;
  line-height: 1.4;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.7rem;
  color: #999;
  padding-top: 0.5rem;
  border-top: 1px solid #e0e0e0;
}

.ubicacion {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.alertas-list {
  list-style: none;
  padding: 0;
  margin: 0 0 0.75rem 0;
}

.alertas-list li {
  margin-bottom: 0.75rem;
}

.alerta-item {
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 3px solid;
}

.alerta-item.alto {
  border-color: #dc3545;
  background-color: #f8d7da;
}

.alerta-item.medio {
  border-color: #ffc107;
  background-color: #fff3cd;
}

.alerta-item.bajo {
  border-color: #0dcaf0;
  background-color: #cff4fc;
}

.alerta-item strong {
  display: block;
  margin-bottom: 0.25rem;
  font-size: 0.85rem;
}

.alerta-item p {
  margin: 0 0 0.25rem 0;
  font-size: 0.75rem;
}

.view-all {
  display: block;
  text-align: right;
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.85rem;
}

.view-all:hover {
  text-decoration: underline;
}

.quick-actions {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  width: 100%;
  max-width: 100%;
}

.action-btn {
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: opacity 0.3s;
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-btn:hover {
  opacity: 0.9;
}
</style>
