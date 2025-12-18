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
      <div v-if="menuOpen" class="mobile-menu">
        <div class="mobile-menu-content">
          <!-- User Info Section -->
          <div class="menu-user-info">
            <div class="user-avatar">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="8" r="4"/>
                <path d="M6 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2"/>
              </svg>
            </div>
            <strong>{{ authStore.user?.nombre || 'Usuario' }}</strong>
            <span class="role-badge">{{ formatRole(authStore.userRole) }}</span>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAlertaStore } from '@/stores/alerta'
import { useNotificacionStore } from '@/stores/notificacion'

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

function handleEditProfile() {
  closeMenu()
  router.push('/perfil')
}

async function handleLogout() {
  closeMenu()
  await authStore.logout()
  router.push('/login')
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
  }
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  overflow-x: hidden;
}

/* ===== NAVBAR ===== */
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 1000;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  width: 100%;
  max-width: 100vw;
}

.nav-brand a {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Notification Icon */
.notif-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  color: #666;
  text-decoration: none;
  border-radius: 50%;
  transition: all 0.2s;
}

.notif-icon:hover {
  background-color: #f0f0f0;
  color: #667eea;
}

.notif-icon .badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background-color: #dc3545;
  color: white;
  font-size: 0.65rem;
  padding: 0.15rem 0.35rem;
  border-radius: 10px;
  font-weight: 600;
  min-width: 18px;
  text-align: center;
}

/* Hamburger Button */
.hamburger-btn {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1002;
  position: relative;
}

.hamburger-btn span {
  width: 100%;
  height: 3px;
  background-color: #333;
  border-radius: 3px;
  transition: all 0.3s ease;
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
  background: white;
  z-index: 1001;
  overflow-y: auto;
  padding-top: 60px;
}

.mobile-menu-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* User Info Section */
.menu-user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.user-avatar svg {
  stroke: white;
}

.menu-user-info strong {
  font-size: 1.1rem;
  text-align: center;
}

.role-badge {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.menu-divider {
  height: 1px;
  background: #e0e0e0;
  margin: 0.5rem 0;
}

/* Navigation Links */
.menu-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  color: #333;
  text-decoration: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}

.menu-link svg {
  flex-shrink: 0;
  stroke: #666;
  transition: stroke 0.2s;
}

.menu-link:hover,
.menu-link.router-link-active {
  background: #f0f0f0;
  color: #667eea;
}

.menu-link:hover svg,
.menu-link.router-link-active svg {
  stroke: #667eea;
}

.menu-badge {
  margin-left: auto;
  background-color: #dc3545;
  color: white;
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-weight: 600;
  min-width: 22px;
  text-align: center;
}

/* Action Buttons */
.menu-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.menu-action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  color: #333;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-action-btn svg {
  flex-shrink: 0;
}

.menu-action-btn:hover {
  background: #f8f9fa;
  border-color: #667eea;
  color: #667eea;
}

.menu-action-btn.logout {
  border-color: #dc3545;
  color: #dc3545;
}

.menu-action-btn.logout:hover {
  background: #ffebee;
  border-color: #dc3545;
}

/* Slide Transition */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}

/* Main Content */
.main-content {
  width: 100%;
  max-width: 100vw;
  margin: 0;
  padding: 0;
  margin-top: 56px; /* Altura aproximada del navbar */
  overflow-x: hidden;
}
</style>
