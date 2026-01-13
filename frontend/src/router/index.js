import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Splash',
    component: () => import('@/views/SplashView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mapa',
    name: 'Mapa',
    component: () => import('@/views/MapaView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/incidencias',
    name: 'Incidencias',
    component: () => import('@/views/IncidenciasView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mis-incidencias',
    name: 'MisIncidencias',
    component: () => import('@/views/MisIncidenciasView.vue'),
    meta: { requiresAuth: true, roles: ['ciudadano'] }
  },
  {
    path: '/incidencias/nueva',
    name: 'NuevaIncidencia',
    component: () => import('@/views/NuevaIncidenciaView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/incidencias/:id',
    name: 'DetalleIncidencia',
    component: () => import('@/views/DetalleIncidenciaView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/alertas',
    name: 'Alertas',
    component: () => import('@/views/AlertasView.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'operador'] }
  },
  {
    path: '/notificaciones',
    name: 'Notificaciones',
    component: () => import('@/views/NotificacionesView.vue'),
    meta: { requiresAuth: true, roles: ['ciudadano'] }
  },
  {
    path: '/perfil',
    name: 'Perfil',
    component: () => import('@/views/PerfilView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Si hay una posición guardada (navegación hacia atrás/adelante), usarla
    if (savedPosition) {
      return savedPosition
    }
    // Si hay un hash (#), hacer scroll a ese elemento
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    // Por defecto, hacer scroll al top
    return { top: 0, behavior: 'smooth' }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Ruta requiere autenticación
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // Ruta solo para invitados (login/register)
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
    return
  }
  
  // Verificar roles
  if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    next({ name: 'Dashboard' })
    return
  }
  
  next()
})

export default router
