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

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.dashboard-content {
  padding: 40px 20px;
  max-width: 1000px;
  margin: 0 auto;
  animation: fadeIn 0.6s ease;
}

h1 {
  font-size: 42px;
  font-weight: 900;
  margin-bottom: 32px;
  color: var(--text-dark);
  letter-spacing: -0.03em;
  animation: slideUp 0.5s ease;
}

h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--text-dark);
  letter-spacing: -0.02em;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 40px;
  width: 100%;
  max-width: 100%;
}

.stat-card {
  background: var(--bg-white);
  padding: 24px;
  border-radius: var(--radius-xl);
  border: 2px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
  overflow: hidden;
  transition: all var(--transition-base);
  position: relative;
  animation: scaleIn 0.5s ease backwards;
}

.stat-card:nth-child(1) { animation-delay: 0.1s; }
.stat-card:nth-child(2) { animation-delay: 0.2s; }
.stat-card:nth-child(3) { animation-delay: 0.3s; }
.stat-card:nth-child(4) { animation-delay: 0.4s; }

.stat-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 0%, rgba(0,0,0,0.02) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.stat-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: var(--shadow-xl);
  border-color: var(--text-dark);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-icon {
  font-size: 32px;
  flex-shrink: 0;
  animation: float 3s ease-in-out infinite;
}

.stat-info {
  min-width: 0;
  overflow: hidden;
}

.stat-info h3 {
  font-size: 32px;
  font-weight: 900;
  margin: 0;
  color: var(--text-dark);
  letter-spacing: -0.02em;
}

.stat-info p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dashboard-sections {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
  margin-bottom: 32px;
  width: 100%;
  max-width: 100%;
}

.section {
  background: var(--bg-white);
  padding: 28px;
  border-radius: var(--radius-xl);
  border: 2px solid var(--border-light);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  transition: all var(--transition-base);
  animation: slideUp 0.6s ease backwards;
  animation-delay: 0.3s;
}

.section:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--text-secondary);
}

.loading, .empty {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
}

.incidencias-grid {
  display: grid;
  gap: 12px;
  margin-bottom: 16px;
  width: 100%;
  max-width: 100%;
}

.incidencia-card {
  background: var(--bg-light);
  border-radius: var(--radius-lg);
  padding: 16px;
  cursor: pointer;
  transition: all var(--transition-base);
  border: 2px solid transparent;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

.incidencia-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.03) 100%);
  opacity: 0;
  transition: opacity var(--transition-base);
  pointer-events: none;
}

.incidencia-card:hover {
  transform: translateX(8px);
  box-shadow: var(--shadow-md);
  border-color: var(--text-dark);
  background: var(--bg-white);
}

.incidencia-card:hover::after {
  opacity: 1;
}

.incidencia-card:active {
  transform: translateX(4px) scale(0.98);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 8px;
}

.codigo-badge {
  background: var(--text-dark);
  color: white;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.estado-badge {
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.estado-badge.abierta {
  background-color: var(--warning);
  color: #000;
}

.estado-badge.en_progreso {
  background-color: var(--info);
  color: #000;
}

.estado-badge.resuelta {
  background-color: var(--success);
  color: #000;
}

.card-body {
  margin-bottom: 12px;
}

.tipo-incidencia {
  font-weight: 700;
  color: var(--text-dark);
  font-size: 15px;
  margin-bottom: 6px;
  letter-spacing: -0.01em;
}

.descripcion {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--text-tertiary);
  padding-top: 12px;
  border-top: 2px solid var(--border-light);
  gap: 8px;
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
  margin: 0 0 16px 0;
}

.alertas-list li {
  margin-bottom: 12px;
}

.alerta-item {
  padding: 16px;
  border-radius: var(--radius-lg);
  border-left: 4px solid;
  background: var(--bg-light);
  transition: all var(--transition-base);
}

.alerta-item:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow-sm);
}

.alerta-item.alto {
  border-color: var(--error);
  background-color: rgba(255, 68, 68, 0.08);
}

.alerta-item.medio {
  border-color: var(--warning);
  background-color: rgba(255, 204, 0, 0.08);
}

.alerta-item.bajo {
  border-color: var(--info);
  background-color: rgba(0, 204, 255, 0.08);
}

.alerta-item strong {
  display: block;
  margin-bottom: 6px;
  font-size: 15px;
  color: var(--text-dark);
  font-weight: 700;
}

.alerta-item p {
  margin: 0 0 6px 0;
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.alerta-item .fecha {
  font-size: 12px;
  color: var(--text-tertiary);
  font-weight: 600;
}

.view-all {
  display: inline-flex;
  align-items: center;
  color: var(--text-dark);
  text-decoration: none;
  font-weight: 700;
  font-size: 15px;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
  border: 2px solid transparent;
}

.view-all:hover {
  background: var(--text-dark);
  color: white;
  transform: translateX(4px);
}

.quick-actions {
  background: var(--text-dark);
  padding: 32px 28px;
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
  animation: slideUp 0.6s ease backwards;
  animation-delay: 0.5s;
}

.quick-actions::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 100%);
  pointer-events: none;
}

.quick-actions h2 {
  color: white;
  margin-bottom: 20px;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  width: 100%;
  max-width: 100%;
}

.action-btn {
  padding: 16px;
  background: white;
  border: 2px solid white;
  color: var(--text-dark);
  text-align: center;
  text-decoration: none;
  border-radius: var(--radius-lg);
  font-weight: 700;
  font-size: 14px;
  transition: all var(--transition-base);
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  position: relative;
  letter-spacing: -0.01em;
}

.action-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--text-dark);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--transition-base);
  z-index: 0;
}

.action-btn > * {
  position: relative;
  z-index: 1;
}

.action-btn:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  color: white;
}

.action-btn:hover::before {
  transform: scaleX(1);
}

.action-btn:active {
  transform: translateY(-2px);
}
</style>
