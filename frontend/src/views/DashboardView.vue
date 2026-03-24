<template>
  <AppLayout>
    <div class="dashboard-content">
      <!-- Dashboard para Ciudadanos -->
      <div v-if="authStore.isCiudadano" class="ciudadano-dashboard">
        <!-- Acciones Rápidas -->
        <section class="acciones-rapidas">
          <div class="actions-grid">
            <router-link to="/incidencias/nueva" class="action-card">
              <img class="action-icon" src="/icons/dashboard/nuevaincidencia.png" alt="" loading="lazy" decoding="async" />
              <span>Nueva Incidencia</span>
            </router-link>
            
            <router-link to="/mapa" class="action-card">
              <img class="action-icon" src="/icons/dashboard/mapa.png" alt="" loading="lazy" decoding="async" />
              <span>Ver Mapa</span>
            </router-link>
            
            <router-link to="/mis-incidencias" class="action-card">
              <img class="action-icon" src="/icons/dashboard/lista-de-quehaceres.png" alt="" loading="lazy" decoding="async" />
              <span>Mis Incidencias</span>
            </router-link>
            
            <router-link to="/notificaciones" class="action-card">
              <img class="action-icon" src="/icons/dashboard/notificacion.png" alt="" loading="lazy" decoding="async" />
              <span>Notificaciones</span>
            </router-link>
          </div>
        </section>

        <!-- Incidencias Activas Recientes -->
        <section class="incidencias-section">
          <h2>Incidencias Activas Recientes</h2>
          <div v-if="isLoading" class="loading">Cargando...</div>
          <div v-else-if="incidenciasActivas.length === 0" class="empty">
            No hay incidencias activas
          </div>
          <div v-else class="incidencias-list">
            <div 
              v-for="incidencia in incidenciasActivas.slice(0, 5)" 
              :key="incidencia.id"
              class="incidencia-card"
              @click="$router.push(`/incidencias/${incidencia.id}`)"
            >
              <div class="card-header">
                <span class="codigo-badge">{{ incidencia.codigo_unico }}</span>
                <span :class="['estado-badge', incidencia.estado]">
                  {{ formatEstado(incidencia.estado) }}
                </span>
              </div>
              <div class="card-body">
                <div class="tipo-incidencia">{{ formatTipo(incidencia.tipo) }}</div>
                <p class="descripcion">{{ truncateText(incidencia.descripcion, 80) }}</p>
              </div>
              <div class="card-footer">
                <span class="fecha">📅 {{ formatDate(incidencia.fecha_creacion) }}</span>
                <span class="ubicacion" v-if="incidencia.ubicacion">📍 {{ incidencia.ubicacion }}</span>
              </div>
              <div v-if="incidencia.comentarios_count > 0" class="comentarios-preview">
                💬 {{ incidencia.comentarios_count }} {{ incidencia.comentarios_count === 1 ? 'comentario' : 'comentarios' }}
              </div>
              <div class="card-action">
                <span class="ver-detalles">Ver Detalles →</span>
              </div>
            </div>
            <div v-if="incidenciasActivas.length > 5" class="ver-mas-container">
              <button class="btn-ver-mas" @click="$router.push('/incidencias')">Ver más incidencias</button>
            </div>
          </div>
        </section>

        <!-- Consejos de Seguridad -->
        <section class="consejos-seguridad">
          <h2>💡 Consejos de Seguridad</h2>
          <div class="consejos-list">
            <div class="consejo-card">
              <div class="consejo-icon">🚨</div>
              <p>Ante una emergencia, llama al 112 antes de reportar la incidencia</p>
            </div>
            <div class="consejo-card">
              <div class="consejo-icon">📸</div>
              <p>Toma fotos de la escena para facilitar la resolución</p>
            </div>
            <div class="consejo-card">
              <div class="consejo-icon">📍</div>
              <p>Reporta con la ubicación exacta para respuesta más rápida</p>
            </div>
            <div class="consejo-card">
              <div class="consejo-icon">🔔</div>
              <p>Activa las notificaciones para seguir el estado de tus reportes</p>
            </div>
          </div>
        </section>
      </div>

      <!-- Dashboard para Seguridad -->
      <div v-else class="seguridad-dashboard">
        <!-- Mi Incidencia Asignada -->
        <section v-if="miIncidenciaAsignada" class="mi-incidencia">
          <h2>Mi Incidencia Asignada</h2>
          <div class="incidencia-asignada" @click="$router.push(`/incidencias/${miIncidenciaAsignada.id}`)">
            <div class="card-header">
              <span class="codigo-badge">{{ miIncidenciaAsignada.codigo_unico }}</span>
              <span :class="['estado-badge', miIncidenciaAsignada.estado]">
                {{ formatEstado(miIncidenciaAsignada.estado) }}
              </span>
            </div>
            <div class="card-body">
              <div class="tipo-incidencia">{{ miIncidenciaAsignada.tipo }}</div>
              <p class="descripcion">{{ miIncidenciaAsignada.descripcion }}</p>
            </div>
            <div class="card-footer">
              <span class="fecha">📅 {{ formatDate(miIncidenciaAsignada.fecha_creacion) }}</span>
              <span class="ubicacion" v-if="miIncidenciaAsignada.ubicacion">📍 {{ miIncidenciaAsignada.ubicacion }}</span>
            </div>
            <div v-if="miIncidenciaAsignada.comentarios_count > 0" class="comentarios-preview">
              💬 {{ miIncidenciaAsignada.comentarios_count }} {{ miIncidenciaAsignada.comentarios_count === 1 ? 'comentario' : 'comentarios' }}
            </div>
            <div class="card-action">
              <button class="btn-gestionar">Gestionar Incidencia</button>
            </div>
          </div>
        </section>

        <!-- Incidencias Sin Asignar -->
        <section class="incidencias-libres-section">
          <h2>Incidencias Sin Asignar</h2>
          <div v-if="isLoading" class="loading">Cargando...</div>
          <div v-else-if="incidenciasLibres.length === 0" class="empty">
            No hay incidencias sin asignar
          </div>
          <div v-else class="incidencias-list">
            <div 
              v-for="incidencia in incidenciasLibres.slice(0, 5)" 
              :key="incidencia.id"
              class="incidencia-card libre"
              @click="$router.push(`/incidencias/${incidencia.id}`)"
            >
              <div class="card-header">
                <span class="codigo-badge">{{ incidencia.codigo_unico }}</span>
                <span class="tiempo-espera">⏱️ {{ tiempoEspera(incidencia.fecha_creacion) }}</span>
              </div>
              <div class="card-body">
                <div class="tipo-incidencia">{{ formatTipo(incidencia.tipo) }}</div>
                <p class="descripcion">{{ truncateText(incidencia.descripcion, 80) }}</p>
              </div>
              <div class="card-footer">
                <span class="fecha">📅 {{ formatDate(incidencia.fecha_creacion) }}</span>
                <span class="ubicacion" v-if="incidencia.ubicacion">📍 {{ incidencia.ubicacion }}</span>
              </div>
              <div v-if="incidencia.comentarios_count > 0" class="comentarios-preview">
                💬 {{ incidencia.comentarios_count }} {{ incidencia.comentarios_count === 1 ? 'comentario' : 'comentarios' }}
              </div>
              <div class="card-action">
                <span class="ver-detalles">Tomar Incidencia →</span>
              </div>
            </div>
            <div v-if="incidenciasLibres.length > 5" class="ver-mas-container">
              <button class="btn-ver-mas" @click="$router.push('/incidencias')">Ver más incidencias</button>
            </div>
          </div>
        </section>

        <!-- Estadísticas -->
        <section class="estadisticas">
          <h2>Estadísticas</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">📊</div>
              <div class="stat-info">
                <h3>{{ estadisticas.total }}</h3>
                <p>Total</p>
              </div>
            </div>
            
            <div class="stat-card pendientes">
              <div class="stat-icon">⚠️</div>
              <div class="stat-info">
                <h3>{{ estadisticas.pendientes }}</h3>
                <p>Pendientes</p>
              </div>
            </div>
            
            <div class="stat-card proceso">
              <div class="stat-icon">⚙️</div>
              <div class="stat-info">
                <h3>{{ estadisticas.enProceso }}</h3>
                <p>En Proceso</p>
              </div>
            </div>
            
            <div class="stat-card resueltas">
              <div class="stat-icon">✅</div>
              <div class="stat-info">
                <h3>{{ estadisticas.resueltas }}</h3>
                <p>Resueltas</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useIncidenciaStore } from '@/stores/incidencia'
import AppLayout from '@/layouts/AppLayout.vue'

const authStore = useAuthStore()
const incidenciaStore = useIncidenciaStore()

const isLoading = ref(false)

// Para ciudadanos: incidencias activas (todas excepto resueltas) ordenadas por más recientes
const incidenciasActivas = computed(() => {
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  return incidencias
    .filter(i => i.estado !== 'resuelta')
    .sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion))
    .slice(0, 10) // Mostrar las 10 más recientes
})

// Para seguridad: mi incidencia asignada
const miIncidenciaAsignada = computed(() => {
  if (!authStore.user?.id) return null
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  return incidencias.find(i => 
    i.asignado_a === authStore.user.id && 
    i.estado !== 'resuelta'
  )
})

// Para seguridad: incidencias sin asignar, ordenadas por más antiguas primero
const incidenciasLibres = computed(() => {
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  return incidencias
    .filter(i => !i.asignado_a && i.estado !== 'resuelta')
    .sort((a, b) => new Date(a.fecha_creacion) - new Date(b.fecha_creacion)) // Más antiguas primero
    .slice(0, 20) // Mostrar las 20 más antiguas
})

// Estadísticas para operadores
const estadisticas = computed(() => {
  const incidencias = Array.isArray(incidenciaStore.incidencias) ? incidenciaStore.incidencias : []
  return {
    total: incidencias.length,
    pendientes: incidencias.filter(i => i.estado === 'abierta').length,
    enProceso: incidencias.filter(i => i.estado === 'en_progreso').length,
    resueltas: incidencias.filter(i => i.estado === 'resuelta').length
  }
})

function formatEstado(estado) {
  const estados = {
    'abierta': 'Pendiente',
    'en_progreso': 'En Proceso',
    'resuelta': 'Resuelta'
  }
  return estados[estado] || estado
}

function formatTipo(tipo) {
  const tipos = {
    'robo': 'Robo',
    'vandalismo': 'Vandalismo',
    'accidente': 'Accidente',
    'incendio': 'Incendio',
    'situacion_incomoda': 'Situación Incómoda',
    'estafa': 'Estafa',
    'otro': 'Otro'
  }
  return tipos[tipo] || tipo
}

function formatDate(dateString) {
  if (!dateString) return ''
  
  const fecha = new Date(dateString)
  const ahora = new Date()
  const diffMs = ahora - fecha
  const diffMins = Math.floor(diffMs / 60000)
  const diffHoras = Math.floor(diffMs / 3600000)
  const diffDias = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return 'Ahora mismo'
  if (diffMins < 60) return `Hace ${diffMins}m`
  if (diffHoras < 24) return `Hace ${diffHoras}h`
  if (diffDias < 7) return `Hace ${diffDias}d`
  
  return fecha.toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short'
  })
}

function tiempoEspera(dateString) {
  if (!dateString) return ''
  
  const fecha = new Date(dateString)
  const ahora = new Date()
  const diffMs = ahora - fecha
  const diffMins = Math.floor(diffMs / 60000)
  const diffHoras = Math.floor(diffMs / 3600000)
  const diffDias = Math.floor(diffMs / 86400000)
  
  if (diffMins < 60) return `${diffMins}m esperando`
  if (diffHoras < 24) return `${diffHoras}h esperando`
  return `${diffDias}d esperando`
}

function truncateText(text, maxLength) {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

onMounted(async () => {
  isLoading.value = true
  try {
    await incidenciaStore.fetchAll()
  } catch (error) {
    console.error('Error cargando incidencias:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
:root {
  --success: #00ff88;
  --warning: #ffcc00;
  --info: #00ccff;
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --transition-base: all 0.3s ease;
}

.dashboard-content {
  padding: 1rem 1rem 2rem;
  max-width: 600px;
  margin: 0 auto;
  background: #000;
  min-height: 100vh;
}

h1 {
  font-size: 32px;
  font-weight: 900;
  margin-bottom: 24px;
  color: #fff;
  letter-spacing: -0.03em;
}

h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #fff;
  letter-spacing: -0.02em;
}

section {
  margin-bottom: 32px;
}

/* Acciones Rápidas */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-card {
  background: linear-gradient(135deg, #00ff88 0%, #00cc70 100%);
  border: none;
  padding: 16px 12px;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: #000;
  font-weight: 700;
  font-size: 13px;
  transition: var(--transition-base);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
}

.action-card:active {
  transform: scale(0.95);
}

.action-icon {
  width: 28px;
  height: 28px;
  object-fit: contain;
  display: block;
}

/* Incidencias */
.incidencias-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.incidencia-card {
  background: #fff;
  border: 2px solid #e0e0e0;
  padding: 16px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: var(--transition-base);
}

.incidencia-card:active {
  transform: scale(0.98);
}

.incidencia-card.libre {
  border-color: var(--success);
}

.incidencia-asignada {
  background: #fff;
  border: 3px solid var(--success);
  padding: 20px;
  border-radius: var(--radius-lg);
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  gap: 8px;
}

.codigo-badge {
  background: #000;
  color: #fff;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
}

.estado-badge {
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
  border: 2px solid;
}

.estado-badge.abierta {
  background: rgba(255, 204, 0, 0.2);
  color: #000;
  border-color: var(--warning);
}

.estado-badge.en_progreso {
  background: rgba(0, 204, 255, 0.2);
  color: #000;
  border-color: var(--info);
}

.estado-badge.resuelta {
  background: rgba(0, 255, 136, 0.2);
  color: #000;
  border-color: var(--success);
}

.tiempo-espera {
  background: rgba(255, 204, 0, 0.2);
  color: #000;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 11px;
  font-weight: 700;
  border: 2px solid var(--warning);
}

.card-body {
  margin-bottom: 12px;
}

.tipo-incidencia {
  font-weight: 700;
  color: #000;
  font-size: 15px;
  margin-bottom: 6px;
  text-transform: capitalize;
}

.descripcion {
  color: #666;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.card-footer {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.comentarios-preview {
  background: rgba(0, 204, 255, 0.1);
  color: #000;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
  border: 1px solid rgba(0, 204, 255, 0.3);
}

.card-action {
  margin-top: 8px;
  text-align: right;
}

.ver-detalles {
  color: #000;
  font-weight: 900;
  font-size: 14px;
}

.btn-gestionar {
  width: 100%;
  background: var(--success);
  color: #000;
  border: none;
  padding: 12px;
  border-radius: var(--radius-md);
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: var(--transition-base);
}

.btn-gestionar:active {
  transform: scale(0.95);
}

.btn-ver-mas {
  background: #fff;
  color: #111;
  border: 2px solid #00ff88;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: 700;
  padding: 0.75rem 2.5rem;
  margin: 24px auto 0 auto;
  display: block;
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-ver-mas:hover {
  background: #00ff88;
  color: #fff;
  border-color: #00ff88;
}

/* Estadísticas */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.stat-card {
  background: #fff;
  border: 2px solid #e0e0e0;
  padding: 20px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-card.pendientes {
  border-color: var(--warning);
}

.stat-card.proceso {
  border-color: var(--info);
}

.stat-card.resueltas {
  border-color: var(--success);
}

.stat-icon {
  font-size: 28px;
}

.stat-info h3 {
  font-size: 24px;
  font-weight: 900;
  color: #000;
  margin: 0 0 4px 0;
}

.stat-info p {
  font-size: 12px;
  color: #666;
  margin: 0;
}

/* Consejos de Seguridad */
.consejos-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.consejo-card {
  background: #1a1a1a;
  border: 2px solid #333;
  border-left: 4px solid var(--success);
  padding: 14px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 12px;
}

.consejo-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.consejo-card p {
  color: #ccc;
  font-size: 13px;
  margin: 0;
  line-height: 1.5;
}

/* Estados */
.loading, .empty {
  text-align: center;
  padding: 32px 16px;
  color: #666;
  font-size: 14px;
}

/* Responsive */
@media (max-width: 400px) {
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
