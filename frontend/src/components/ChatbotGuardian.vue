<template>
  <div class="chatbot-container">
    <!-- Botón flotante -->
    <button 
      v-if="!isOpen" 
      @click="toggleChat" 
      class="chat-button"
      aria-label="Abrir chat con El Guardián"
    >
      <span class="chat-icon">💬</span>
      <span v-if="hasUnreadMessage" class="notification-dot"></span>
    </button>

    <!-- Ventana de chat -->
    <div v-if="isOpen" class="chat-window">
      <!-- Header -->
      <div class="chat-header">
        <div class="header-info">
          <div class="avatar">🛡️</div>
          <div class="guardian-info">
            <h3>El Guardián</h3>
            <span class="status">En línea</span>
          </div>
        </div>
        <button @click="toggleChat" class="close-button">✕</button>
      </div>

      <!-- Mensajes -->
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.sender]"
        >
          <div class="message-bubble">
            <p v-html="message.text"></p>
            <span class="timestamp">{{ message.time }}</span>
          </div>
        </div>
        
        <!-- Typing indicator -->
        <div v-if="isTyping" class="message guardian">
          <div class="message-bubble typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>

      <!-- Opciones rápidas -->
      <div v-if="showQuickOptions" class="quick-options">
        <button 
          v-for="option in quickOptions" 
          :key="option.value"
          @click="selectOption(option.value)"
          class="quick-option-btn"
        >
          {{ option.label }}
        </button>
      </div>

      <!-- Input -->
      <div class="chat-input">
        <input 
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="Escribe tu mensaje..."
          :disabled="isTyping"
        />
        <button 
          @click="sendMessage" 
          :disabled="!userInput.trim() || isTyping"
          class="send-button"
        >
          ➤
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const isOpen = ref(false)
const hasUnreadMessage = ref(false)
const userInput = ref('')
const messages = ref([])
const isTyping = ref(false)
const messagesContainer = ref(null)
const showQuickOptions = ref(false)
const currentContext = ref('initial') // initial, funcionalidades, clasificacion

const quickOptions = ref([
  { label: '📱 Ayuda con funcionalidades', value: 'funcionalidades' },
  { label: '🏷️ Clasificar incidencia', value: 'clasificacion' }
])

const tiposIncidencia = [
  { value: 'robo', label: 'Robo', desc: 'Sustracción de pertenencias' },
  { value: 'accidente', label: 'Accidente', desc: 'Incidente vehicular o lesión' },
  { value: 'incendio', label: 'Incendio', desc: 'Fuego o humo' },
  { value: 'vandalismo', label: 'Vandalismo', desc: 'Daño a propiedad' },
  { value: 'situacion_incomoda', label: 'Situación Incómoda', desc: 'Acoso o comportamiento inapropiado' },
  { value: 'estafa', label: 'Estafa', desc: 'Fraude o engaño' },
  { value: 'otro', label: 'Otro', desc: 'Otro tipo de incidencia' }
]

function toggleChat() {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    hasUnreadMessage.value = false
    if (messages.value.length === 0) {
      initializeChat()
    }
    scrollToBottom()
  }
}

function initializeChat() {
  const userName = authStore.user?.nombre || authStore.user?.username || 'Usuario'
  
  addMessage(
    `¡Hola, ${userName}! 👋<br><br>Soy <strong>El Guardián</strong>, tu asistente virtual.<br><br>¿En qué puedo ayudarte hoy?`,
    'guardian'
  )
  
  showQuickOptions.value = true
  currentContext.value = 'initial'
}

function addMessage(text, sender = 'user') {
  const now = new Date()
  const time = now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
  
  messages.value.push({
    text,
    sender,
    time
  })
  
  nextTick(() => scrollToBottom())
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

async function selectOption(option) {
  showQuickOptions.value = false
  
  if (option === 'funcionalidades') {
    addMessage('Ayuda con funcionalidades de la app', 'user')
    await simulateTyping()
    showFuncionalidadesHelp()
  } else if (option === 'clasificacion') {
    addMessage('Ayuda para clasificar mi incidencia', 'user')
    await simulateTyping()
    showClasificacionHelp()
  }
}

function showFuncionalidadesHelp() {
  const role = authStore.user?.tipo || 'normal'
  
  let helpText = `<strong>📱 Funcionalidades disponibles:</strong><br><br>`
  
  if (role === 'normal') {
    helpText += `
      <strong>🆕 Reportar Incidencia:</strong><br>
      Crea una nueva incidencia con fotos/videos y ubicación.<br><br>
      
      <strong>📋 Ver Incidencias:</strong><br>
      Consulta todas las incidencias del campus.<br><br>
      
      <strong>📊 Mis Incidencias:</strong><br>
      Revisa el estado de tus reportes.<br><br>
      
      <strong>🔔 Notificaciones:</strong><br>
      Recibe actualizaciones sobre tus incidencias.<br><br>
      
      <strong>👤 Perfil:</strong><br>
      Actualiza tu información personal.
    `
  } else if (role === 'operador') {
    helpText += `
      <strong>📋 Gestión de Incidencias:</strong><br>
      Revisa y gestiona las incidencias asignadas.<br><br>
      
      <strong>🚨 Alertas:</strong><br>
      Recibe notificaciones de nuevas incidencias.<br><br>
      
      <strong>📊 Dashboard:</strong><br>
      Visualiza estadísticas y métricas.
    `
  } else if (role === 'admin') {
    helpText += `
      <strong>⚙️ Administración Completa:</strong><br>
      Gestiona usuarios, incidencias y configuración del sistema.<br><br>
      
      <strong>📊 Analytics:</strong><br>
      Accede a reportes y estadísticas avanzadas.
    `
  }
  
  addMessage(helpText, 'guardian')
  
  setTimeout(() => {
    addMessage('¿Necesitas ayuda con algo más?', 'guardian')
    showQuickOptions.value = true
    currentContext.value = 'initial'
  }, 1500)
}

function showClasificacionHelp() {
  addMessage(
    `<strong>🏷️ Clasificación de Incidencias:</strong><br><br>
    Te ayudaré a identificar el tipo correcto. Descríbeme brevemente qué ocurrió:<br><br>
    <em>Ejemplo: "Vi humo saliendo de un edificio"</em>`,
    'guardian'
  )
  
  currentContext.value = 'clasificacion'
}

async function sendMessage() {
  if (!userInput.value.trim()) return
  
  const message = userInput.value
  addMessage(message, 'user')
  userInput.value = ''
  
  await simulateTyping()
  
  if (currentContext.value === 'clasificacion') {
    classifyIncident(message)
  } else {
    handleGeneralQuery(message)
  }
}

function classifyIncident(description) {
  const lowerDesc = description.toLowerCase()
  
  let matchedType = null
  
  // Palabras clave para cada tipo
  const keywords = {
    robo: ['robaron', 'robo', 'robado', 'sustrajeron', 'me quitaron', 'hurto', 'ladrón'],
    accidente: ['accidente', 'choque', 'caída', 'lesión', 'herido', 'golpe', 'caí'],
    incendio: ['fuego', 'incendio', 'humo', 'llamas', 'quemando', 'arde'],
    vandalismo: ['rayado', 'roto', 'vandalismo', 'graffiti', 'daño', 'destruido', 'pintado'],
    situacion_incomoda: ['acoso', 'incómodo', 'hostigamiento', 'persiguiendo', 'miedo', 'amenaza'],
    estafa: ['estafa', 'fraude', 'engaño', 'timaron', 'prometieron'],
    otro: ['otro', 'diferente', 'extraño']
  }
  
  // Buscar coincidencias
  for (const [tipo, words] of Object.entries(keywords)) {
    if (words.some(word => lowerDesc.includes(word))) {
      matchedType = tipo
      break
    }
  }
  
  if (matchedType) {
    const tipoInfo = tiposIncidencia.find(t => t.value === matchedType)
    addMessage(
      `Basándome en tu descripción, esto parece ser un caso de:<br><br>
      <strong>✅ ${tipoInfo.label}</strong><br>
      <em>${tipoInfo.desc}</em><br><br>
      ¿Es correcto? Si necesitas reportar esta incidencia, usa el botón "Reportar Incidencia" en el menú.`,
      'guardian'
    )
  } else {
    addMessage(
      `No estoy seguro del tipo exacto. Aquí están todas las categorías:<br><br>
      ${tiposIncidencia.map(t => `<strong>${t.label}:</strong> ${t.desc}`).join('<br>')}<br><br>
      ¿Cuál describe mejor tu situación?`,
      'guardian'
    )
  }
  
  setTimeout(() => {
    addMessage('¿Puedo ayudarte con algo más?', 'guardian')
    showQuickOptions.value = true
    currentContext.value = 'initial'
  }, 2000)
}

function handleGeneralQuery(query) {
  const lowerQuery = query.toLowerCase()
  
  // Respuestas basadas en palabras clave
  if (lowerQuery.includes('cómo') && lowerQuery.includes('reportar')) {
    addMessage(
      `Para reportar una incidencia:<br><br>
      1. Ve a "Reportar Incidencia" en el menú<br>
      2. Selecciona el tipo de incidencia<br>
      3. Describe lo ocurrido<br>
      4. Marca la ubicación en el mapa<br>
      5. Adjunta fotos o videos (opcional)<br>
      6. Envía el reporte<br><br>
      ¡Recibirás notificaciones sobre el progreso!`,
      'guardian'
    )
  } else if (lowerQuery.includes('notificacion')) {
    addMessage(
      `Las notificaciones te informan sobre:<br><br>
      • Cambios de estado en tus incidencias<br>
      • Cuando se asigna personal de seguridad<br>
      • Cuando se resuelve tu caso<br><br>
      Activas automáticamente en "Notificaciones" del menú.`,
      'guardian'
    )
  } else {
    addMessage(
      `Entiendo tu consulta. ¿Quieres que te ayude con:<br><br>
      • Funcionalidades de la app<br>
      • Clasificar una incidencia<br><br>
      Selecciona una opción abajo.`,
      'guardian'
    )
    showQuickOptions.value = true
  }
}

async function simulateTyping() {
  isTyping.value = true
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000))
  isTyping.value = false
}

onMounted(() => {
  // Mostrar notificación después de 5 segundos si no ha abierto el chat
  setTimeout(() => {
    if (!isOpen.value && messages.value.length === 0) {
      hasUnreadMessage.value = true
    }
  }, 5000)
})
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.chat-button {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.4);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  padding: 0;
  line-height: 1;
}

.chat-button:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(0, 255, 136, 0.6);
}

.chat-icon {
  font-size: 28px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 16px;
  height: 16px;
  background: #ff4444;
  border-radius: 50%;
  border: 3px solid #000;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.chat-window {
  width: 380px;
  height: 600px;
  background: #000;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 2px solid #00ff88;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.chat-header {
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #00ff88;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  background: #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  border: 2px solid #000;
}

.guardian-info h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #000;
}

.status {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.7);
}

.close-button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  border: none;
  color: #000;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  line-height: 1;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.2);
  transform: rotate(90deg);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #000;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #00ff88;
  border-radius: 3px;
}

.message {
  display: flex;
  animation: messageSlide 0.3s ease;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.guardian {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 16px;
  position: relative;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  color: #000;
  border-bottom-right-radius: 4px;
}

.message.guardian .message-bubble {
  background: #1a1a1a;
  color: #fff;
  border: 1px solid #333;
  border-bottom-left-radius: 4px;
}

.message-bubble p {
  margin: 0;
  line-height: 1.5;
  font-size: 14px;
}

.timestamp {
  font-size: 11px;
  opacity: 0.6;
  margin-top: 4px;
  display: block;
}

.typing {
  display: flex;
  gap: 4px;
  padding: 16px;
}

.typing span {
  width: 8px;
  height: 8px;
  background: #00ff88;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.quick-options {
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #000;
  border-top: 1px solid #333;
}

.quick-option-btn {
  padding: 12px 16px;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 12px;
  color: #00ff88;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.quick-option-btn:hover {
  background: #00ff88;
  color: #000;
  transform: translateX(4px);
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 16px 20px;
  background: #000;
  border-top: 1px solid #333;
}

.chat-input input {
  flex: 1;
  padding: 12px 16px;
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 24px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.chat-input input:focus {
  border-color: #00ff88;
  background: #0a0a0a;
}

.chat-input input::placeholder {
  color: #666;
}

.send-button {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #00ff88 0%, #00cc6f 100%);
  border: none;
  border-radius: 50%;
  color: #000;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 255, 136, 0.4);
}

.send-button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .chat-window {
    width: calc(100vw - 32px);
    height: calc(100vh - 100px);
    bottom: 16px;
    right: 16px;
  }
  
  .chatbot-container {
    bottom: 16px;
    right: 16px;
  }
}
</style>
