from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone

from app_models.models import Usuario, Incidencia, Alerta, Notificacion, ArchivoIncidencia, Comentario
from .serializers import (
    UsuarioSerializer, 
    IncidenciaSerializer, 
    IncidenciaCreateSerializer,
    AlertaSerializer,
    RegisterSerializer,
    NotificacionSerializer,
    ComentarioSerializer
)

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Endpoint de health check para mantener el servicio activo.
    GET /api/health/
    """
    return Response({
        "status": "healthy",
        "timestamp": timezone.now().isoformat()
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Endpoint para login de usuarios.
    POST /api/auth/login/
    Espera: { "email": "user@example.com", "password": "password" }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {"message": "Email y contraseña son requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Buscar usuario por email
    try:
        usuario = Usuario.objects.get(email=email)
        username = usuario.username
    except Usuario.DoesNotExist:
        return Response(
            {"message": "Credenciales inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Autenticar
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        # Usar el serializer para obtener todos los datos del usuario
        serializer = UsuarioSerializer(user, context={'request': request})
        
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': serializer.data
        })
    else:
        return Response(
            {"message": "Credenciales inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Endpoint para registrar nuevos usuarios.
    POST /api/auth/register/
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Usuario registrado exitosamente"},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    - list: Listar todos los usuarios (solo admin)
    - retrieve: Ver perfil de usuario
    - update: Actualizar perfil
    - destroy: Eliminar usuario (solo admin)
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """Configurar permisos según la acción"""
        if self.action in ['list', 'destroy']:
            # Solo staff puede listar todos o eliminar
            permission_classes = [IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        """Sobrescribir update para usar partial=True siempre"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Sobrescribir partial_update para asegurar partial=True"""
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_incidencias(self, request):
        """Obtener incidencias del usuario actual"""
        incidencias = Incidencia.objects.filter(usuario=request.user)
        serializer = IncidenciaSerializer(incidencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_alertas(self, request):
        """Obtener alertas del usuario actual"""
        alertas = Alerta.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        serializer = AlertaSerializer(alertas, many=True)
        return Response(serializer.data)


class IncidenciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar incidencias.
    - list: Listar todas las incidencias
    - create: Crear nueva incidencia
    - retrieve: Ver detalle de incidencia
    - update: Actualizar incidencia
    - destroy: Eliminar incidencia
    """
    queryset = Incidencia.objects.all().order_by('-fecha_reporte')
    
    def get_permissions(self):
        """Permitir lectura sin autenticación, escritura requiere autenticación"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Usar serializer diferente para creación"""
        if self.action == 'create':
            return IncidenciaCreateSerializer
        return IncidenciaSerializer
    
    def get_queryset(self):
        """Retornar todas las incidencias ordenadas por fecha"""
        return Incidencia.objects.all().order_by('-fecha_reporte')
    
    def create(self, request, *args, **kwargs):
        """Crear incidencia y retornar respuesta completa con todos los campos"""
        # Validar que solo ciudadanos puedan crear incidencias
        if request.user.tipo != 'normal':
            return Response(
                {'error': 'Solo los ciudadanos pueden reportar incidencias'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Extraer archivos del request
        archivos = request.FILES.getlist('archivos')
        print(f"\n{'='*60}")
        print(f"📁 ARCHIVOS RECIBIDOS: {len(archivos)}")
        for idx, archivo in enumerate(archivos):
            print(f"  {idx+1}. Nombre: {archivo.name}")
            print(f"     Tipo: {archivo.content_type}")
            print(f"     Tamaño: {archivo.size / (1024*1024):.2f} MB")
        print(f"{'='*60}\n")
        
        # Copiar datos del request sin los archivos para el serializer
        data = request.data.copy()
        if 'archivos' in data:
            del data['archivos']
        
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            incidencia = serializer.save(usuario=request.user)
            
            # Procesar archivos manualmente
            archivos_guardados = 0
            for archivo in archivos:
                try:
                    # Determinar tipo basado en el content_type
                    content_type = archivo.content_type
                    print(f"\n🔍 Procesando archivo: {archivo.name} ({content_type})")
                    
                    if content_type.startswith('image/'):
                        tipo = 'imagen'
                        resource_type = 'image'
                    elif content_type.startswith('video/'):
                        tipo = 'video'
                        resource_type = 'video'
                    else:
                        print(f"⚠️  Tipo de archivo no soportado: {content_type}")
                        continue  # Ignorar archivos que no sean imágenes o videos
                    
                    print(f"💾 Guardando como: {tipo} (resource_type={resource_type})")
                    
                    # Subir directamente a Cloudinary con el resource_type correcto
                    import cloudinary.uploader
                    from django.core.files.uploadedfile import InMemoryUploadedFile
                    
                    upload_result = cloudinary.uploader.upload(
                        archivo,
                        resource_type=resource_type,
                        folder='incidencias'
                    )
                    
                    cloudinary_url = upload_result.get('secure_url')
                    print(f"✅ Cloudinary upload exitoso: {cloudinary_url}")
                    
                    # Crear el objeto ArchivoIncidencia sin guardar aún
                    archivo_obj = ArchivoIncidencia(
                        incidencia=incidencia,
                        tipo=tipo
                    )
                    
                    # Asignar el nombre del archivo manualmente
                    # Cloudinary devuelve public_id que podemos usar
                    archivo_obj.archivo.name = f"incidencias/{upload_result.get('public_id')}"
                    archivo_obj.save()
                    
                    print(f"✅ Archivo guardado con ID: {archivo_obj.id}")
                    archivos_guardados += 1
                    
                except Exception as e:
                    print(f"❌ ERROR al procesar archivo {archivo.name}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Continuar con los demás archivos
            
            print(f"\n📊 RESUMEN: {archivos_guardados}/{len(archivos)} archivos guardados correctamente\n")
            
            # Usar el serializer completo para la respuesta
            response_serializer = IncidenciaSerializer(incidencia, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"ERROR al crear incidencia: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al crear la incidencia: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario actual al crear incidencia"""
        # Establecer valores por defecto
        incidencia = serializer.save(usuario=self.request.user)
        return incidencia
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado de una incidencia (solo usuarios de seguridad)"""
        if request.user.tipo != 'seguridad' and not request.user.is_staff:
            return Response(
                {"detail": "Solo usuarios de seguridad pueden cambiar el estado"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        incidencia = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        # Mapear estados del frontend al backend
        estado_map = {
            'abierta': 'pendiente',
            'en_progreso': 'en_proceso',
            'resuelta': 'resuelta'
        }
        
        estado_backend = estado_map.get(nuevo_estado, nuevo_estado)
        
        if estado_backend not in dict(Incidencia.ESTADOS):
            return Response(
                {"detail": "Estado inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Si se marca como "en_proceso", verificar que no esté ya asignada a otro usuario
        if estado_backend == 'en_proceso':
            if incidencia.asignado_a and incidencia.asignado_a != request.user:
                return Response(
                    {"detail": f"Esta incidencia ya está siendo atendida por {incidencia.asignado_a.nombre}"},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Asignar al usuario actual
            incidencia.asignado_a = request.user
        elif estado_backend == 'pendiente':
            # Si se vuelve a abrir, liberar la asignación
            incidencia.asignado_a = None
        
        incidencia.estado = estado_backend
        incidencia.save()
        serializer = self.get_serializer(incidencia)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resolver(self, request, pk=None):
        """Resolver una incidencia con nota (solo personal de seguridad)"""
        if request.user.tipo != 'seguridad' and not request.user.is_staff:
            return Response(
                {"detail": "Solo personal de seguridad puede resolver incidencias"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        incidencia = self.get_object()
        nota = request.data.get('nota_resolucion', '')
        
        if not nota:
            return Response(
                {"detail": "Debe proporcionar una nota de resolución"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar la incidencia
        incidencia.estado = 'resuelta'
        incidencia.nota_resolucion = nota
        incidencia.resuelto_por = request.user
        from django.utils import timezone
        incidencia.fecha_resolucion = timezone.now()
        incidencia.save()
        
        serializer = self.get_serializer(incidencia)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        """Filtrar incidencias por tipo"""
        tipo = request.query_params.get('tipo', None)
        if tipo:
            incidencias = self.get_queryset().filter(tipo=tipo)
        else:
            incidencias = self.get_queryset()
        
        serializer = self.get_serializer(incidencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """Filtrar incidencias por estado"""
        estado = request.query_params.get('estado', None)
        if estado:
            incidencias = self.get_queryset().filter(estado=estado)
        else:
            incidencias = self.get_queryset()
        
        serializer = self.get_serializer(incidencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mapa(self, request):
        """
        Obtener incidencias en formato GeoJSON para Leaflet.
        Endpoint especial para mostrar todas las incidencias en el mapa.
        """
        incidencias = self.get_queryset()
        
        # Crear estructura GeoJSON
        features = []
        for incidencia in incidencias:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(incidencia.longitud), float(incidencia.latitud)]
                },
                "properties": {
                    "id": incidencia.id,
                    "titulo": incidencia.titulo,
                    "descripcion": incidencia.descripcion,
                    "tipo": incidencia.tipo,
                    "estado": incidencia.estado,
                    "direccion": incidencia.direccion,
                    "fecha_reporte": incidencia.fecha_reporte.isoformat(),
                    "usuario": incidencia.usuario.username,
                }
            }
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)


class AlertaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar alertas.
    """
    serializer_class = AlertaSerializer
    
    def get_permissions(self):
        """Permitir lectura sin autenticación, escritura requiere autenticación"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Retornar solo las alertas del usuario actual ordenadas por fecha"""
        if self.request.user.is_authenticated:
            return Alerta.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
        return Alerta.objects.none()
    
    def perform_create(self, serializer):
        """
        Crear alerta. Si no hay incidencia, crear una genérica.
        """
        # Por ahora, las alertas requieren incidencia
        # Necesitarás crear una incidencia primero o modificar el modelo
        serializer.save(usuario=self.request.user)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def marcar_leida(self, request, pk=None):
        """Marcar alerta como leída"""
        alerta = self.get_object()
        alerta.estado = 'leida'
        alerta.save()
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Obtener alertas pendientes del usuario"""
        alertas = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar notificaciones de ciudadanos
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retornar solo notificaciones del usuario actual"""
        queryset = Notificacion.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
        # Logging desactivado para no llenar los logs
        # print(f"[NOTIF] Usuario solicitante: {self.request.user.username}")
        # print(f"[NOTIF] Notificaciones encontradas: {queryset.count()}")
        return queryset
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def marcar_leida(self, request, pk=None):
        """Marcar notificación como leída"""
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        serializer = self.get_serializer(notificacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Obtener notificaciones no leídas del usuario"""
        notificaciones = self.get_queryset().filter(leida=False)
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def count_no_leidas(self, request):
        """Contar notificaciones no leídas"""
        count = self.get_queryset().filter(leida=False).count()
        return Response({'count': count})


class ComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet para comentarios de incidencias"""
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtra comentarios por incidencia si se proporciona el parámetro"""
        queryset = Comentario.objects.all()
        incidencia_id = self.request.query_params.get('incidencia', None)
        if incidencia_id:
            queryset = queryset.filter(incidencia_id=incidencia_id)
        return queryset.select_related('usuario', 'incidencia')
    
    def perform_create(self, serializer):
        """Asigna automáticamente el usuario actual al crear el comentario"""
        serializer.save(usuario=self.request.user)


