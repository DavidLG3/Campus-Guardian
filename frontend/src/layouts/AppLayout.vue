<template>
  <div class="app-layout">
    <nav class="navbar">
      <div class="nav-content">
        <!-- Logo/Brand -->
        <div class="nav-brand">
          <router-link to="/dashboard">🛡️ Campus Guardian</router-link>
        </div>
        
        <!-- Notification Bell (solo ciudadanos) -->
        <router-link 
          v-if="authStore.isCiudadano" 
          to="/notificaciones"
          class="notif-icon"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
          </svg>
          <span v-if="notificacionesNoLeidas > 0" class="badge">{{ notificacionesNoLeidas }}</span>
        </router-link>
        
        <!-- Hamburger Menu Button -->
        <button @click="toggleMenu" class="hamburger-btn" :class="{ active: menuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
    
    <!-- Fullscreen Mobile Menu -->
    <transition name="slide">
      <div v-if="menuOpen" class="mobile-menu" @click.self="closeMenu">
        <div class="mobile-menu-content">
          <!-- User Info Section -->
          <div class="menu-header">
            <div class="user-avatar">
              <img v-if="authStore.user?.foto_perfil_url" :src="authStore.user.foto_perfil_url" alt="Avatar" class="avatar-image" />
              <span v-else class="avatar-initials">{{ getInitials() }}</span>
            </div>
            <div class="user-details">
              <strong>{{ authStore.user?.nombre || 'Usuario' }}</strong>
              <span class="role-badge">{{ formatRole(authStore.userRole) }}</span>
            </div>
            <button @click="closeMenu" class="menu-close-btn" title="Cerrar menú">
              ✕
            </button>
          </div>
          
          <div class="menu-divider"></div>
          
          <!-- Navigation Links -->
          <nav class="menu-nav">
            <router-link to="/dashboard" @click="closeMenu" class="menu-link">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="7" height="7"/>
                <rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/>
                <rect x="3" y="14" width="7" height="7"/>
              </svg>
              Dashboard
            </router-link>
            
            <router-link to="/mapa" @click="closeMenu" class="menu-link">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/>
                <line x1="8" y1="2" x2="8" y2="18"/>
                <line x1="16" y1="6" x2="16" y2="22"/>
              </svg>
              Mapa
            </router-link>
            
            <router-link to="/incidencias" @click="closeMenu" class="menu-link">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              Incidencias
            </router-link>
            
            <router-link 
              v-if="authStore.isCiudadano" 
              to="/mis-incidencias" 
              @click="closeMenu" 
              class="menu-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="8.5" cy="7" r="4"/>
                <line x1="20" y1="8" x2="20" y2="14"/>
                <line x1="23" y1="11" x2="17" y2="11"/>
              </svg>
              Mis Incidencias
            </router-link>
            
            <router-link 
              v-if="authStore.isAdmin || authStore.isOperador" 
              to="/alertas" 
              @click="closeMenu" 
              class="menu-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              Alertas
              <span v-if="alertasNoLeidas > 0" class="menu-badge">{{ alertasNoLeidas }}</span>
            </router-link>
            
            <router-link 
              v-if="authStore.isCiudadano" 
              to="/notificaciones" 
              @click="closeMenu" 
              class="menu-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
              Notificaciones
              <span v-if="notificacionesNoLeidas > 0" class="menu-badge">{{ notificacionesNoLeidas }}</span>
            </router-link>
          </nav>
          
          <div class="menu-divider"></div>
          
          <!-- Action Buttons -->
          <div class="menu-actions">
            <button @click="handleEditProfile" class="menu-action-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              Editar Perfil
            </button>
            
            <button @click="handleLogout" class="menu-action-btn logout">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <main class="main-content">
      <slot />
    </main>
    
    <!-- Chatbot Guardian -->
    <ChatbotGuardian />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAlertaStore } from '@/stores/alerta'
import { useNotificacionStore } from '@/stores/notificacion'
import ChatbotGuardian from '@/components/ChatbotGuardian.vue'

const router = useRouter()
const authStore = useAuthStore()
const alertaStore = useAlertaStore()
const notificacionStore = useNotificacionStore()
const menuOpen = ref(false)

const alertasNoLeidas = computed(() => {
  try {
    return alertaStore.countNoLeidas || 0
  } catch (err) {
    console.error('Error calculando alertas no leídas:', err)
    return 0
  }
})

const notificacionesNoLeidas = computed(() => {
  try {
    return notificacionStore.countNoLeidas || 0
  } catch (err) {
    console.error('Error calculando notificaciones no leídas:', err)
    return 0
  }
})

// Intervalo para polling de alertas/notificaciones
let pollingInterval = null

const startPolling = () => {
  // Consultar cada 3 segundos para actualizaciones casi en tiempo real
  pollingInterval = setInterval(() => {
    if (authStore.isAuthenticated) {
      // Solo hacer polling de alertas si NO estamos en la vista de alertas
      if (authStore.isAdmin || authStore.isOperador) {
        if (router.currentRoute.value.path !== '/alertas') {
          alertaStore.fetchAll().catch(err => {
            console.error('Error en polling de alertas:', err)
          })
        }
      }
      // Solo hacer polling de notificaciones si NO estamos en la vista de notificaciones
      if (authStore.isCiudadano) {
        if (router.currentRoute.value.path !== '/notificaciones') {
          notificacionStore.fetchAll().catch(err => {
            console.error('Error en polling de notificaciones:', err)
          })
        }
      }
    }
  }, 3000) // 3 segundos
}

const stopPolling = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
}

function formatRole(role) {
  const roles = {
    'admin': 'Administrador',
    'operador': 'Operador',
    'ciudadano': 'Ciudadano'
  }
  return roles[role] || role
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

function closeMenu() {
  menuOpen.value = false
}

function getInitials() {
  const nombre = authStore.user?.nombre || authStore.user?.email || 'U'
  return nombre.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2)
}

function handleEditProfile() {
  closeMenu()
  router.push('/perfil')
}

async function handleLogout() {
  closeMenu()
  await authStore.logout()
  router.push('/')
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    if (authStore.isAdmin || authStore.isOperador) {
      alertaStore.fetchAll().catch(err => {
        console.error('Error cargando alertas en AppLayout:', err)
      })
    }
    if (authStore.isCiudadano) {
      notificacionStore.fetchAll().catch(err => {
        console.error('Error cargando notificaciones en AppLayout:', err)
      })
    }
    
    // Iniciar polling para actualizaciones en tiempo real
    startPolling()
  }
})

onUnmounted(() => {
  // Limpiar el intervalo al desmontar el componente
  stopPolling()
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  background-color: var(--bg-light);
  overflow-x: hidden;
}

/* ===== MODERN NAVBAR =====  */
.navbar {
  background: var(--bg-white);
  border-bottom: 2px solid var(--border-light);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 1000;
  backdrop-filter: blur(10px);
  transition: all var(--transition-base);
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  width: 100%;
  max-width: 100vw;
}

.nav-brand a {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-dark);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-fast);
  letter-spacing: -0.03em;
}

.nav-brand a:hover {
  transform: scale(1.02);
}

/* Notification Icon with pulse animation */
.notif-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  color: var(--text-dark);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.notif-icon:hover {
  background-color: var(--bg-light);
  transform: scale(1.1);
}

.notif-icon .badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: var(--text-dark);
  color: white;
  font-size: 10px;
  padding: 3px 6px;
  border-radius: var(--radius-full);
  font-weight: 700;
  min-width: 18px;
  text-align: center;
  line-height: 1.2;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* Modern Hamburger Button */
.hamburger-btn {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  z-index: 1002;
  position: relative;
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.hamburger-btn:hover {
  background: var(--bg-light);
  transform: scale(1.05);
}

.hamburger-btn span {
  width: 100%;
  height: 3px;
  background-color: var(--text-dark);
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
  transform-origin: center;
}

.hamburger-btn.active span:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.hamburger-btn.active span:nth-child(2) {
  opacity: 0;
  transform: translateX(-20px);
}

.hamburger-btn.active span:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

/* ===== MOBILE MENU ===== */
.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: #fff;
  z-index: 1001;
  overflow-y: auto;
}

.mobile-menu-content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Menu Header with User Info */
.menu-header {
  background: linear-gradient(135deg, #000 0%, #1a1a1a 100%);
  padding: 32px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
}

.menu-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.3), transparent);
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  border: 3px solid rgba(0, 255, 136, 0.3);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
}

.user-avatar .avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-avatar .avatar-initials {
  font-size: 24px;
  font-weight: 900;
  color: #000;
  text-transform: uppercase;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.user-details strong {
  font-size: 18px;
  font-weight: 800;
  color: white;
  line-height: 1.2;
}

.menu-header .role-badge {
  background: rgba(0, 255, 136, 0.15);
  color: #00ff88;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(0, 255, 136, 0.3);
  display: inline-block;
  width: fit-content;
}

.menu-close-btn {
  width: 40px;
  height: 40px;
  background: transparent !important;
  border: none !important;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  font-size: 32px;
  color: #00ff88 !important;
  font-weight: 300;
  line-height: 1;
  transition: none !important;
  transform: none !important;
  pointer-events: auto;
}

.menu-close-btn:hover,
.menu-close-btn:active,
.menu-close-btn:focus {
  background: transparent !important;
  color: #00ff88 !important;
  transform: none !important;
  transition: none !important;
}

.menu-divider {
  height: 1px;
  background: #e5e5e5;
  margin: 0 24px;
}

/* Navigation Links with smooth animations */
.menu-nav {
  display: flex;
  flex-direction: column;
  padding: 24px 12px;
  gap: 8px;
  flex: 1;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  color: #1a1a1a;
  text-decoration: none;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 600;
  transition: all 0.3s ease;
  position: relative;
  background: transparent;
}

.menu-link:hover {
  background: #f5f5f5;
  color: #000;
}

.menu-link.router-link-active {
  background: linear-gradient(135deg, #00ff88, #00dd77);
  color: #000;
}

.menu-link svg {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
}

.menu-link svg {
  flex-shrink: 0;
  stroke: var(--text-dark);
  transition: all var(--transition-base);
  z-index: 1;
}

.menu-link:hover {
  background: var(--bg-light);
  transform: translateX(4px);
}

.menu-link:hover::before {
  width: 4px;
}

.menu-link.router-link-active {
  background: var(--text-dark);
  color: white;
  transform: translateX(0);
}

.menu-link.router-link-active::before {
  width: 0;
}

.menu-link.router-link-active svg {
  stroke: white;
}

.menu-badge {
  margin-left: auto;
  background: var(--text-dark);
  color: white;
  font-size: 11px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-weight: 700;
  min-width: 20px;
  text-align: center;
  line-height: 1.2;
  animation: pulse 2s infinite;
}

/* Action Buttons with hover effects */
.menu-actions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
  padding: 0 12px 24px 12px;
}

.menu-action-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 24px;
  background: var(--bg-white);
  border: 2px solid var(--border-light);
  border-radius: var(--radius-lg);
  color: var(--text-dark);
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.menu-action-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--text-dark);
  transform: translateY(100%);
  transition: transform var(--transition-base);
}

.menu-action-btn svg {
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  stroke: var(--text-dark);
  transition: stroke var(--transition-base);
  z-index: 1;
}

.menu-action-btn > span {
  z-index: 1;
}

.menu-action-btn:hover {
  border-color: var(--text-dark);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.menu-action-btn:hover::before {
  transform: translateY(0);
}

.menu-action-btn:hover svg {
  stroke: white;
}

.menu-action-btn.logout {
  color: var(--error);
  border-color: var(--error);
}

.menu-action-btn.logout::before {
  background: var(--error);
}

.menu-action-btn.logout svg {
  stroke: var(--error);
}

.menu-action-btn.logout:hover {
  color: white;
  border-color: var(--error);
}

.menu-action-btn.logout:hover svg {
  stroke: white;
}

/* Slide Transition - smoother */
.slide-enter-active,
.slide-leave-active {
  transition: transform var(--transition-slow), opacity var(--transition-base);
}

.slide-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* Main Content */
.main-content {
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  margin-top: 66px; /* Altura del navbar */
  overflow-x: hidden;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
