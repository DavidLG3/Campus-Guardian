<template>
  <div class="media-capture">
    <!-- Botones de acción -->
    <div v-if="!capturing" class="action-buttons">
      <button type="button" @click="selectFiles" class="btn-action">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
        Seleccionar archivos
      </button>
      
      <button type="button" @click="startPhotoCapture" class="btn-action">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
          <circle cx="12" cy="13" r="4"/>
        </svg>
        Tomar foto
      </button>
      
      <button type="button" @click="startVideoCapture" class="btn-action">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="23 7 16 12 23 17 23 7"/>
          <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
        </svg>
        Grabar video
      </button>
    </div>
    
    <!-- Input oculto para seleccionar archivos -->
    <input 
      ref="fileInput" 
      type="file" 
      accept="image/*,video/*" 
      multiple 
      style="display: none"
      @change="handleFileSelect"
    />
    
    <!-- Captura de foto -->
    <div v-if="capturing === 'photo'" class="capture-container">
      <video ref="photoVideo" autoplay playsinline class="video-preview"></video>
      <div class="capture-controls">
        <button type="button" @click="capturePhoto" class="btn-capture">
          📸 Capturar
        </button>
        <button type="button" @click="stopCapture" class="btn-cancel">
          Cancelar
        </button>
      </div>
    </div>
    
    <!-- Captura de video -->
    <div v-if="capturing === 'video'" class="capture-container">
      <video ref="videoRecorder" autoplay playsinline class="video-preview"></video>
      <div class="capture-controls">
        <button v-if="!recording" type="button" @click="startRecording" class="btn-capture">
          ⏺ Grabar
        </button>
        <button v-else type="button" @click="stopRecording" class="btn-stop">
          ⏹ Detener
        </button>
        <span v-if="recording" class="recording-indicator">
          🔴 Grabando... {{ recordingTime }}s
        </span>
        <button type="button" @click="stopCapture" class="btn-cancel">
          Cancelar
        </button>
      </div>
    </div>
    
    <!-- Preview de archivos seleccionados -->
    <div v-if="files.length > 0" class="files-preview">
      <h4>Archivos seleccionados ({{ files.length }})</h4>
      <div class="files-grid">
        <div v-for="(file, index) in files" :key="index" class="file-item">
          <div class="file-preview">
            <img v-if="file.type.startsWith('image/')" :src="file.preview" alt="Preview" />
            <video v-else-if="file.type.startsWith('video/')" :src="file.preview" controls></video>
            <div v-else class="file-icon">📄</div>
          </div>
          <div class="file-info">
            <span class="file-name">{{ file.name }}</span>
            <span class="file-size">{{ formatFileSize(file.size) }}</span>
          </div>
          <button type="button" @click="removeFile(index)" class="btn-remove" title="Eliminar">
            ✕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'

const emit = defineEmits(['files-selected'])

const fileInput = ref(null)
const photoVideo = ref(null)
const videoRecorder = ref(null)
const capturing = ref(null) // null, 'photo', 'video'
const recording = ref(false)
const recordingTime = ref(0)
const files = ref([])

let stream = null
let mediaRecorder = null
let recordedChunks = []
let recordingInterval = null

// Seleccionar archivos desde galería
const selectFiles = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  selectedFiles.forEach(file => {
    const preview = URL.createObjectURL(file)
    files.value.push({
      file,
      preview,
      name: file.name,
      size: file.size,
      type: file.type
    })
  })
  
  // Resetear input
  event.target.value = ''
  
  emitFiles()
}

// Iniciar captura de foto
const startPhotoCapture = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' },
      audio: false 
    })
    capturing.value = 'photo'
    
    // Esperar al siguiente tick para que el video esté en el DOM
    setTimeout(() => {
      if (photoVideo.value) {
        photoVideo.value.srcObject = stream
      }
    }, 100)
  } catch (error) {
    console.error('Error al acceder a la cámara:', error)
    alert('No se pudo acceder a la cámara. Verifica los permisos.')
  }
}

// Capturar foto
const capturePhoto = () => {
  const video = photoVideo.value
  const canvas = document.createElement('canvas')
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  const ctx = canvas.getContext('2d')
  ctx.drawImage(video, 0, 0)
  
  canvas.toBlob((blob) => {
    const file = new File([blob], `foto_${Date.now()}.jpg`, { type: 'image/jpeg' })
    const preview = URL.createObjectURL(blob)
    
    files.value.push({
      file,
      preview,
      name: file.name,
      size: file.size,
      type: file.type
    })
    
    stopCapture()
    emitFiles()
  }, 'image/jpeg', 0.9)
}

// Iniciar captura de video
const startVideoCapture = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' },
      audio: true 
    })
    capturing.value = 'video'
    
    setTimeout(() => {
      if (videoRecorder.value) {
        videoRecorder.value.srcObject = stream
      }
    }, 100)
  } catch (error) {
    console.error('Error al acceder a la cámara:', error)
    alert('No se pudo acceder a la cámara. Verifica los permisos.')
  }
}

// Iniciar grabación de video
const startRecording = () => {
  recordedChunks = []
  
  const options = { mimeType: 'video/webm;codecs=vp8,opus' }
  
  try {
    mediaRecorder = new MediaRecorder(stream, options)
  } catch (e) {
    // Fallback si el formato no es soportado
    mediaRecorder = new MediaRecorder(stream)
  }
  
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recordedChunks.push(event.data)
    }
  }
  
  mediaRecorder.onstop = () => {
    const blob = new Blob(recordedChunks, { type: 'video/webm' })
    const file = new File([blob], `video_${Date.now()}.webm`, { type: 'video/webm' })
    const preview = URL.createObjectURL(blob)
    
    files.value.push({
      file,
      preview,
      name: file.name,
      size: file.size,
      type: file.type
    })
    
    stopCapture()
    emitFiles()
  }
  
  mediaRecorder.start()
  recording.value = true
  recordingTime.value = 0
  
  // Contador de tiempo
  recordingInterval = setInterval(() => {
    recordingTime.value++
  }, 1000)
}

// Detener grabación
const stopRecording = () => {
  if (mediaRecorder && recording.value) {
    mediaRecorder.stop()
    recording.value = false
    clearInterval(recordingInterval)
  }
}

// Detener captura y liberar recursos
const stopCapture = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  
  if (recording.value) {
    stopRecording()
  }
  
  capturing.value = null
  
  if (photoVideo.value) {
    photoVideo.value.srcObject = null
  }
  
  if (videoRecorder.value) {
    videoRecorder.value.srcObject = null
  }
}

// Eliminar archivo
const removeFile = (index) => {
  URL.revokeObjectURL(files.value[index].preview)
  files.value.splice(index, 1)
  emitFiles()
}

// Emitir archivos al componente padre
const emitFiles = () => {
  emit('files-selected', files.value.map(f => f.file))
}

// Formatear tamaño de archivo
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// Limpiar recursos al desmontar
onUnmounted(() => {
  stopCapture()
  files.value.forEach(file => {
    URL.revokeObjectURL(file.preview)
  })
})

// Exponer método para limpiar desde el padre
defineExpose({
  clearFiles: () => {
    files.value.forEach(file => {
      URL.revokeObjectURL(file.preview)
    })
    files.value = []
    emitFiles()
  }
})
</script>

<style scoped>
.media-capture {
  margin: 20px 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: white;
  border: 2px solid #e5e5e5;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-action:hover {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.05);
  transform: translateY(-2px);
}

.btn-action svg {
  flex-shrink: 0;
}

.capture-container {
  background: #000;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
}

.video-preview {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  display: block;
}

.capture-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #1a1a1a;
}

.btn-capture, .btn-stop {
  padding: 12px 24px;
  background: #00ff88;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 700;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-capture:hover, .btn-stop:hover {
  background: #00dd77;
  transform: scale(1.05);
}

.btn-stop {
  background: #ff4444;
  color: white;
}

.btn-stop:hover {
  background: #dd3333;
}

.btn-cancel {
  padding: 12px 24px;
  background: transparent;
  border: 2px solid #666;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: auto;
}

.btn-cancel:hover {
  border-color: #999;
  background: rgba(255, 255, 255, 0.1);
}

.recording-indicator {
  color: #ff4444;
  font-weight: 600;
  font-size: 14px;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.files-preview {
  background: #f5f5f5;
  border-radius: 12px;
  padding: 16px;
}

.files-preview h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.file-item {
  background: white;
  border-radius: 8px;
  padding: 8px;
  position: relative;
  border: 2px solid #e5e5e5;
  transition: all 0.3s ease;
}

.file-item:hover {
  border-color: #00ff88;
}

.file-preview {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  overflow: hidden;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.file-preview img,
.file-preview video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-icon {
  font-size: 48px;
}

.file-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.file-name {
  font-size: 12px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-size {
  font-size: 11px;
  color: #666;
}

.btn-remove {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 24px;
  height: 24px;
  background: #ff4444;
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  line-height: 1;
}

.btn-remove:hover {
  background: #dd3333;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .btn-action {
    width: 100%;
    justify-content: center;
  }
  
  .files-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
