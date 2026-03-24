<template>
  <div class="avatar-editor-overlay" @click.self="$emit('close')">
    <div class="avatar-editor-modal">
      <div class="modal-header">
        <h3>Editar Foto de Perfil</h3>
        <button @click="$emit('close')" class="close-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <div v-if="!selectedImage && !showCamera" class="upload-options">
        <div class="option-card" @click="triggerFileInput">
          <div class="option-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <circle cx="8.5" cy="8.5" r="1.5"/>
              <polyline points="21 15 16 10 5 21"/>
            </svg>
          </div>
          <h4>Seleccionar Archivo</h4>
          <p>Sube una imagen desde tu dispositivo</p>
        </div>

        <div class="option-card" @click="startCamera">
          <div class="option-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
              <circle cx="12" cy="13" r="4"/>
            </svg>
          </div>
          <h4>Tomar Foto</h4>
          <p>Usa tu cámara para capturar una imagen</p>
        </div>

        <input 
          ref="fileInput" 
          type="file" 
          accept="image/*" 
          @change="handleFileSelect"
          style="display: none"
        />
      </div>

      <div v-if="showCamera" class="camera-container">
        <video ref="videoElement" autoplay playsinline></video>
        <div class="camera-overlay">
          <div class="camera-circle"></div>
        </div>
        <div class="camera-controls">
          <button @click="capturePhoto" class="capture-btn">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="10"/>
            </svg>
          </button>
          <button @click="cancelCamera" class="cancel-camera-btn">Cancelar</button>
        </div>
      </div>

      <div v-if="selectedImage && !showCamera" class="image-preview">
        <div class="crop-container">
          <canvas ref="canvas" 
                  @mousedown="startDrag" 
                  @mousemove="drag" 
                  @mouseup="endDrag"
                  @mouseleave="endDrag"
                  @wheel.prevent="handleZoom"
                  @touchstart.prevent="startDrag"
                  @touchmove.prevent="drag"
                  @touchend="endDrag">
          </canvas>
        </div>
        <div class="crop-instructions">
          <p>📱 Arrastra para posicionar • 🔍 Rueda del ratón para zoom</p>
        </div>
        <div class="preview-actions">
          <button @click="resetImage" class="btn-secondary">Cambiar Foto</button>
          <button @click="saveAvatar" class="btn-primary" :disabled="saving">
            {{ saving ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, nextTick } from 'vue'

const emit = defineEmits(['close', 'save'])

const fileInput = ref(null)
const videoElement = ref(null)
const canvas = ref(null)
const selectedImage = ref(null)
const showCamera = ref(false)
const mediaStream = ref(null)
const saving = ref(false)
const error = ref('')

// Canvas drawing state
const img = ref(null)
const scale = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)
const isDragging = ref(false)
const lastX = ref(0)
const lastY = ref(0)

function triggerFileInput() {
  fileInput.value.click()
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      error.value = 'Por favor selecciona un archivo de imagen'
      return
    }
    const reader = new FileReader()
    reader.onload = (e) => {
      loadImage(e.target.result)
    }
    reader.readAsDataURL(file)
  }
}

async function startCamera() {
  try {
    mediaStream.value = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'user' },
      audio: false 
    })
    showCamera.value = true
    await nextTick()
    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream.value
    }
  } catch (err) {
    error.value = 'No se pudo acceder a la cámara'
    console.error('Error accessing camera:', err)
  }
}

function capturePhoto() {
  const video = videoElement.value
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = video.videoWidth
  tempCanvas.height = video.videoHeight
  const context = tempCanvas.getContext('2d')
  context.drawImage(video, 0, 0)
  const imageData = tempCanvas.toDataURL('image/jpeg')
  cancelCamera()
  loadImage(imageData)
}

function cancelCamera() {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
    mediaStream.value = null
  }
  showCamera.value = false
}

async function loadImage(src) {
  selectedImage.value = src
  await nextTick()
  
  const image = new Image()
  image.onload = () => {
    img.value = image
    initCanvas()
  }
  image.src = src
}

function initCanvas() {
  if (!canvas.value || !img.value) return
  
  const size = 400
  canvas.value.width = size
  canvas.value.height = size
  
  // Calculate initial scale so the image covers the circle
  const imgAspect = img.value.width / img.value.height
  if (imgAspect > 1) {
    scale.value = size / img.value.height
  } else {
    scale.value = size / img.value.width
  }
  
  // Center the image
  offsetX.value = (size - img.value.width * scale.value) / 2
  offsetY.value = (size - img.value.height * scale.value) / 2
  
  drawCanvas()
}

function drawCanvas() {
  if (!canvas.value || !img.value) return
  
  const ctx = canvas.value.getContext('2d')
  const size = canvas.value.width
  
  // Clear canvas
  ctx.clearRect(0, 0, size, size)
  
  // Draw image
  ctx.save()
  ctx.drawImage(
    img.value,
    offsetX.value,
    offsetY.value,
    img.value.width * scale.value,
    img.value.height * scale.value
  )
  ctx.restore()
  
  // Draw overlay with cut-out circle
  ctx.save()
  ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'
  ctx.fillRect(0, 0, size, size)
  ctx.globalCompositeOperation = 'destination-out'
  ctx.beginPath()
  ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
  
  // Draw circle border
  ctx.strokeStyle = '#00ff88'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2)
  ctx.stroke()
}

function getEventCoords(event) {
  const rect = canvas.value.getBoundingClientRect()
  if (event.touches && event.touches.length > 0) {
    return {
      x: event.touches[0].clientX - rect.left,
      y: event.touches[0].clientY - rect.top
    }
  }
  return {
    x: event.clientX - rect.left,
    y: event.clientY - rect.top
  }
}

function startDrag(event) {
  event.preventDefault()
  isDragging.value = true
  const coords = getEventCoords(event)
  lastX.value = coords.x
  lastY.value = coords.y
}

function drag(event) {
  if (!isDragging.value) return
  event.preventDefault()
  
  const coords = getEventCoords(event)
  const dx = coords.x - lastX.value
  const dy = coords.y - lastY.value
  
  offsetX.value += dx
  offsetY.value += dy
  
  lastX.value = coords.x
  lastY.value = coords.y
  
  drawCanvas()
}

function endDrag() {
  isDragging.value = false
}

function handleZoom(event) {
  const delta = event.deltaY > 0 ? 0.9 : 1.1
  const newScale = scale.value * delta
  
  // Limit zoom
  if (newScale < 0.1 || newScale > 5) return
  
  // Zoom toward canvas center
  const size = canvas.value.width
  const centerX = size / 2
  const centerY = size / 2
  
  offsetX.value = centerX - (centerX - offsetX.value) * delta
  offsetY.value = centerY - (centerY - offsetY.value) * delta
  scale.value = newScale
  
  drawCanvas()
}

function resetImage() {
  selectedImage.value = null
  img.value = null
  scale.value = 1
  offsetX.value = 0
  offsetY.value = 0
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

async function saveAvatar() {
  if (!canvas.value || !img.value) {
    error.value = 'No hay imagen para guardar'
    return
  }
  
  saving.value = true
  error.value = ''
  
  try {
    // Create a temporary canvas for final output
    const outputCanvas = document.createElement('canvas')
    const outputSize = 400
    outputCanvas.width = outputSize
    outputCanvas.height = outputSize
    const ctx = outputCanvas.getContext('2d')
    
    // Create circular clip
    ctx.beginPath()
    ctx.arc(outputSize / 2, outputSize / 2, outputSize / 2, 0, Math.PI * 2)
    ctx.clip()
    
    // Draw cropped image
    ctx.drawImage(
      img.value,
      offsetX.value,
      offsetY.value,
      img.value.width * scale.value,
      img.value.height * scale.value
    )
    
    // Convert to blob
    const blob = await new Promise((resolve, reject) => {
      outputCanvas.toBlob((blob) => {
        if (blob) {
          resolve(blob)
        } else {
          reject(new Error('No se pudo crear la imagen'))
        }
      }, 'image/jpeg', 0.9)
    })
    
    emit('save', blob)
    saving.value = false
  } catch (err) {
    console.error('Error al procesar la imagen:', err)
    error.value = 'Error al procesar la imagen: ' + err.message
    saving.value = false
  }
}

onUnmounted(() => {
  cancelCamera()
})
</script>

<style scoped>
.avatar-editor-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.avatar-editor-modal {
  background: #fff;
  border-radius: 24px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 20px 60px rgba(0, 255, 136, 0.3);
  border: 2px solid #00ff88;
  animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

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

.modal-header {
  padding: 2rem;
  border-bottom: 2px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 24px;
  font-weight: 900;
  color: #000;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f0f0f0;
}

.close-btn svg {
  color: #666;
}

.upload-options {
  padding: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.option-card {
  padding: 2rem;
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: #f8f8f8;
}

.option-card:hover {
  border-color: #00ff88;
  background: #fff;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.2);
}

.option-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, #00ff88, #00ccff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.option-icon svg {
  color: #000;
}

.option-card h4 {
  margin: 0 0 0.5rem 0;
  font-size: 18px;
  font-weight: 800;
  color: #000;
}

.option-card p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.camera-container {
  position: relative;
  padding: 2rem;
}

.camera-container video {
  width: 100%;
  border-radius: 16px;
  transform: scaleX(-1);
}

.camera-overlay {
  position: absolute;
  top: 2rem;
  left: 2rem;
  right: 2rem;
  bottom: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.camera-circle {
  width: 300px;
  height: 300px;
  border: 4px solid #00ff88;
  border-radius: 50%;
  box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
}

.camera-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.capture-btn {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #00ff88;
  border: 4px solid #fff;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.capture-btn:hover {
  transform: scale(1.1);
}

.capture-btn svg {
  color: #000;
}

.cancel-camera-btn {
  padding: 1rem 2rem;
  background: transparent;
  color: #666;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-camera-btn:hover {
  border-color: #666;
  color: #000;
}

.image-preview {
  padding: 2rem;
}

.crop-container {
  position: relative;
  background: #f8f8f8;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.crop-container canvas {
  display: block;
  cursor: move;
  user-select: none;
  touch-action: none;
}

.crop-instructions {
  text-align: center;
  margin-bottom: 1.5rem;
}

.crop-instructions p {
  color: #666;
  font-size: 13px;
  margin: 0;
}

.preview-actions {
  display: flex;
  gap: 1rem;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 800;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-secondary {
  background: transparent;
  color: #666;
  border: 2px solid #e0e0e0;
}

.btn-secondary:hover {
  border-color: #666;
  color: #000;
}

.btn-primary {
  background: #00ff88;
  color: #000;
  box-shadow: 0 4px 16px rgba(0, 255, 136, 0.3);
}

.btn-primary:hover:not(:disabled) {
  background: #00dd77;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 255, 136, 0.5);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  margin: 0 2rem 2rem;
  padding: 1rem;
  background: rgba(255, 68, 68, 0.1);
  border: 2px solid rgba(255, 68, 68, 0.3);
  border-radius: 12px;
  color: #ff4444;
  font-weight: 700;
  text-align: center;
}

@media (max-width: 768px) {
  .upload-options {
    grid-template-columns: 1fr;
  }

  .camera-circle {
    width: 200px;
    height: 200px;
  }
}
</style>
