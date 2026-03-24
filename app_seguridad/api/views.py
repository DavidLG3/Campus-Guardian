"""API views for authentication, incidents, alerts, and admin operations."""
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
    Lightweight health check used to verify the API is up.
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
    User login endpoint.
    POST /api/auth/login/
    Expected payload: { "email": "user@example.com", "password": "password" }
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {"message": "Email y contraseña son requeridos"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Find the username linked to the provided email.
    try:
        usuario = Usuario.objects.get(email=email)
        username = usuario.username
    except Usuario.DoesNotExist:
        return Response(
            {"message": "Credenciales inválidas"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Authenticate with Django's auth backend.
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate access and refresh tokens.
        refresh = RefreshToken.for_user(user)
        
        # Return the full user payload through the serializer.
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
    Register a new user account.
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
    ViewSet to manage users.
    - list: List all users (admin only)
    - retrieve: Get user profile
    - update: Update profile
    - destroy: Delete user (admin only)
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get_permissions(self):
        """Set permissions dynamically based on the current action."""
        if self.action in ['list', 'destroy']:
            # Only admins can list all users or delete accounts.
            permission_classes = [IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        """Force partial updates for all update calls."""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Keep partial update behavior explicit and consistent."""
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Return the current authenticated user."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_incidencias(self, request):
        """Return incidents reported by the current user."""
        incidencias = Incidencia.objects.filter(usuario=request.user)
        serializer = IncidenciaSerializer(incidencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_alertas(self, request):
        """Return alerts assigned to the current user."""
        alertas = Alerta.objects.filter(usuario=request.user).order_by('-fecha_creacion')
        serializer = AlertaSerializer(alertas, many=True)
        return Response(serializer.data)


class IncidenciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage incidents.
    - list: List incidents
    - create: Create a new incident
    - retrieve: Get incident details
    - update: Update incident data
    - destroy: Delete an incident
    """
    queryset = Incidencia.objects.all().order_by('-fecha_reporte')
    
    def get_permissions(self):
        """Allow public read access, but require auth for writes."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Use a dedicated serializer when creating incidents."""
        if self.action == 'create':
            return IncidenciaCreateSerializer
        return IncidenciaSerializer
    
    def get_queryset(self):
        """Return incidents ordered by newest first."""
        return Incidencia.objects.all().order_by('-fecha_reporte')
    
    def create(self, request, *args, **kwargs):
        """Create an incident and return a fully serialized response."""
        # Only citizen users can report incidents.
        if request.user.tipo != 'normal':
            return Response(
                {'error': 'Solo los ciudadanos pueden reportar incidencias'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Extract uploaded files from the multipart request.
        archivos = request.FILES.getlist('archivos')
        print(f"\n{'='*60}")
        print(f"📁 ARCHIVOS RECIBIDOS: {len(archivos)}")
        for idx, archivo in enumerate(archivos):
            print(f"  {idx+1}. Nombre: {archivo.name}")
            print(f"     Tipo: {archivo.content_type}")
            print(f"     Tamaño: {archivo.size / (1024*1024):.2f} MB")
        print(f"{'='*60}\n")
        
        # Build serializer input without file objects.
        data = request.data.copy()
        if 'archivos' in data:
            del data['archivos']
        
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            incidencia = serializer.save(usuario=request.user)
            
            # Process uploads manually to control Cloudinary behavior.
            archivos_guardados = 0
            for archivo in archivos:
                try:
                    # Infer file type from content-type.
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
                        # Skip unsupported file types.
                    
                    print(f"💾 Guardando como: {tipo} (resource_type={resource_type})")
                    
                    # Upload directly to Cloudinary with the correct resource type.
                    import cloudinary.uploader
                    from django.core.files.uploadedfile import InMemoryUploadedFile
                    
                    upload_result = cloudinary.uploader.upload(
                        archivo,
                        resource_type=resource_type,
                        folder='incidencias'
                    )
                    
                    cloudinary_url = upload_result.get('secure_url')
                    public_id = upload_result.get('public_id')
                    print(f"✅ Cloudinary upload exitoso: {cloudinary_url}")
                    print(f"   Public ID: {public_id}")
                    
                    # Persist file metadata linked to the new incident.
                    archivo_obj = ArchivoIncidencia.objects.create(
                        incidencia=incidencia,
                        tipo=tipo,
                        cloudinary_public_id=public_id
                    )
                    
                    print(f"✅ Archivo guardado con ID: {archivo_obj.id}")
                    print(f"   URL generada: {archivo_obj.get_cloudinary_url()}")
                    archivos_guardados += 1
                    
                except Exception as e:
                    print(f"❌ ERROR al procesar archivo {archivo.name}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Continue processing remaining files even if one fails.
            
            print(f"\n📊 RESUMEN: {archivos_guardados}/{len(archivos)} archivos guardados correctamente\n")
            
            # Return the full incident payload expected by the frontend.
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
        """Attach the current user automatically on incident creation."""
        # Apply default ownership values during creation.
        incidencia = serializer.save(usuario=self.request.user)
        return incidencia
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def cambiar_estado(self, request, pk=None):
        """Update incident status (security staff only)."""
        if request.user.tipo != 'seguridad' and not request.user.is_staff:
            return Response(
                {"detail": "Solo usuarios de seguridad pueden cambiar el estado"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        incidencia = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        # Map frontend status labels to backend enum values.
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
        
        # If set to in-progress, ensure it is not assigned to someone else.
        if estado_backend == 'en_proceso':
            if incidencia.asignado_a and incidencia.asignado_a != request.user:
                return Response(
                    {"detail": f"Esta incidencia ya está siendo atendida por {incidencia.asignado_a.nombre}"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # A staff member can only handle one in-progress incident at a time.
            incidencias_en_progreso = Incidencia.objects.filter(
                asignado_a=request.user,
                estado='en_proceso'
            ).exclude(id=incidencia.id)
            
            if incidencias_en_progreso.exists():
                incidencia_actual = incidencias_en_progreso.first()
                return Response(
                    {
                        "detail": f"Ya tienes una incidencia en progreso ({incidencia_actual.codigo_unico}). Finalízala antes de tomar otra.",
                        "incidencia_actual": {
                            "id": incidencia_actual.id,
                            "codigo_unico": incidencia_actual.codigo_unico
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Assign ownership to the current user.
            incidencia.asignado_a = request.user
        elif estado_backend == 'pendiente':
            # Re-opening the incident clears assignment.
            incidencia.asignado_a = None
        
        incidencia.estado = estado_backend
        incidencia.save()
        serializer = self.get_serializer(incidencia)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def resolver(self, request, pk=None):
        """Resolve an incident with a mandatory resolution note."""
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
        
        # Save resolution metadata.
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
        """Filter incidents by type."""
        tipo = request.query_params.get('tipo', None)
        if tipo:
            incidencias = self.get_queryset().filter(tipo=tipo)
        else:
            incidencias = self.get_queryset()
        
        serializer = self.get_serializer(incidencias, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_estado(self, request):
        """Filter incidents by status."""
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
        Return incidents as GeoJSON for Leaflet map rendering.
        This endpoint is optimized for map visualization.
        """
        incidencias = self.get_queryset()
        
        # Build a valid GeoJSON FeatureCollection.
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
    ViewSet to manage user alerts.
    """
    serializer_class = AlertaSerializer
    
    def get_permissions(self):
        """Allow public reads, require auth for write operations."""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Return alerts for the current user, newest first."""
        if self.request.user.is_authenticated:
            return Alerta.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
        return Alerta.objects.none()
    
    def perform_create(self, serializer):
        """
        Create an alert linked to the current user.
        """
        # Alerts currently depend on an incident relation.
        serializer.save(usuario=self.request.user)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def marcar_leida(self, request, pk=None):
        """Mark an alert as read."""
        alerta = self.get_object()
        alerta.estado = 'leida'
        alerta.save()
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """Return pending alerts for the current user."""
        alertas = self.get_queryset().filter(estado='pendiente')
        serializer = self.get_serializer(alertas, many=True)
        return Response(serializer.data)


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage citizen notifications.
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the current authenticated user."""
        queryset = Notificacion.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')
        # Keep logging disabled to avoid noisy production logs.
        # print(f"[NOTIF] Usuario solicitante: {self.request.user.username}")
        # print(f"[NOTIF] Notificaciones encontradas: {queryset.count()}")
        return queryset
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def marcar_leida(self, request, pk=None):
        """Mark a notification as read."""
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        serializer = self.get_serializer(notificacion)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Return unread notifications for the current user."""
        notificaciones = self.get_queryset().filter(leida=False)
        serializer = self.get_serializer(notificaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def count_no_leidas(self, request):
        """Return unread notifications count."""
        count = self.get_queryset().filter(leida=False).count()
        return Response({'count': count})


class ComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet for incident comments."""
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter comments by incident when the query param is present."""
        queryset = Comentario.objects.all()
        incidencia_id = self.request.query_params.get('incidencia', None)
        if incidencia_id:
            queryset = queryset.filter(incidencia_id=incidencia_id)
        return queryset.select_related('usuario', 'incidencia')
    
    def perform_create(self, serializer):
        """Attach the current user when creating a comment."""
        serializer.save(usuario=self.request.user)


# Admin endpoints.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_usuarios(request):
    """
    List users with optional type-based filtering.
    GET /api/admin/usuarios/?tipo=normal|seguridad
    Admin access only.
    """
    # Ensure the requester is an admin.
    if request.user.tipo != 'admin':
        return Response(
            {"message": "No tienes permisos para acceder a este recurso"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Read optional filter parameters.
    tipo = request.query_params.get('tipo', None)
    search = request.query_params.get('search', None)
    
    # Build base queryset.
    usuarios = Usuario.objects.all().order_by('-date_joined')
    
    if tipo:
        usuarios = usuarios.filter(tipo=tipo)
    
    if search:
        # Search by name, email, or username.
        from django.db.models import Q
        usuarios = usuarios.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(username__icontains=search)
        )
    
    serializer = UsuarioSerializer(usuarios, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_usuario_seguridad(request):
    """
    Create a new security-staff user.
    POST /api/admin/usuarios/seguridad/
    Admin access only.
    Expected payload: {
        "username": "...",
        "email": "...",
        "password": "...",
        "first_name": "...",
        "last_name": "...",
        "telefono": "..." (opcional)
    }
    """
    # Ensure the requester is an admin.
    if request.user.tipo != 'admin':
        return Response(
            {"message": "No tienes permisos para acceder a este recurso"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Validate required fields.
    required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in request.data:
            return Response(
                {"message": f"El campo {field} es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Check username uniqueness.
    if Usuario.objects.filter(username=request.data['username']).exists():
        return Response(
            {"message": "El nombre de usuario ya está en uso"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check email uniqueness.
    if Usuario.objects.filter(email=request.data['email']).exists():
        return Response(
            {"message": "El email ya está en uso"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the security user.
    try:
        usuario = Usuario.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            telefono=request.data.get('telefono', ''),
            tipo='seguridad'
        )
        
        serializer = UsuarioSerializer(usuario, context={'request': request})
        return Response(
            {
                "message": "Usuario de seguridad creado exitosamente",
                "usuario": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {"message": f"Error al crear usuario: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_usuario(request, pk):
    """
    Delete a user account.
    DELETE /api/admin/usuarios/{id}/
    Admin access only.
    """
    # Ensure the requester is an admin.
    if request.user.tipo != 'admin':
        return Response(
            {"message": "No tienes permisos para acceder a este recurso"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        usuario = Usuario.objects.get(pk=pk)
        
        # Prevent admins from deleting themselves.
        if usuario.id == request.user.id:
            return Response(
                {"message": "No puedes eliminar tu propia cuenta"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent deleting other admin accounts.
        if usuario.tipo == 'admin':
            return Response(
                {"message": "No puedes eliminar otros administradores"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        usuario.delete()
        return Response(
            {"message": "Usuario eliminado exitosamente"},
            status=status.HTTP_200_OK
        )
    except Usuario.DoesNotExist:
        return Response(
            {"message": "Usuario no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_view(request):
    """
    AI chatbot endpoint backed by Google Gemini REST API.
    POST /api/chatbot/
    Expected payload: { "message": "user message", "history": [...] }
    """
    import requests as req
    from django.conf import settings
    
    mensaje_usuario = request.data.get('message')
    historial = request.data.get('history', [])
    
    if not mensaje_usuario:
        return Response(
            {"message": "El mensaje es requerido"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Pull minimal user context for prompt personalization.
        user_tipo = request.user.tipo if hasattr(request.user, 'tipo') else 'normal'
        user_nombre = request.user.nombre if hasattr(request.user, 'nombre') else 'Usuario'
        
        # Keep system prompt compact to reduce latency and token usage.
        contexto_sistema = f"""Eres El Guardián de Campus Guardian (app seguridad UAM).

TIPOS: 🔵Normal (reporta) 🛡️Seguridad (gestiona) 👑Admin (administra)
INCIDENCIAS: Robo, Accidente, Incendio, Situación Incómoda, Vandalismo, Estafa, Otro
ESTADOS: Pendiente → En Proceso → Resuelta
MENÚ: Nueva Incidencia | Ver Incidencias | Mis Incidencias | Dashboard | Notificaciones | Perfil

Usuario: {user_tipo} ({user_nombre})
Responde en español, conciso. Si emergencia: llamar 112."""
        
        # Build prompt with very limited chat history.
        prompt_completo = contexto_sistema + "\n\n"
        
        # Include only the two most recent messages.
        for msg in historial[-2:]:
            sender = "U" if msg.get("sender") == "user" else "G"
            texto = msg.get("text", "").replace("<br>", " ").replace("<strong>", "").replace("</strong>", "")[:100]  # Limitar a 100 caracteres
            prompt_completo += f"{sender}: {texto}\n"
        
        # Append the current user message.
        prompt_completo += f"Usuario: {mensaje_usuario}\nGuardian:"
        
        # Call Gemini REST API using a fast model for chat.
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt_completo
                }]
            }],
            "generationConfig": {
                "temperature": 0.5,
                "topP": 0.8,
                "maxOutputTokens": 800
            }
        }
        
        # Keep request timeout short to avoid hanging responses.
        response = req.post(api_url, json=payload, timeout=30)
        
        # Print API details only when debugging failed calls.
        if response.status_code != 200:
            print(f"Error de API: {response.status_code}")
            print(f"Respuesta: {response.text}")
        
        response.raise_for_status()
        
        result = response.json()
        
        # Extract assistant reply from the API payload.
        if 'candidates' in result and len(result['candidates']) > 0:
            respuesta_texto = result['candidates'][0]['content']['parts'][0]['text']
        else:
            respuesta_texto = "Lo siento, no pude generar una respuesta. ¿Puedes reformular tu pregunta?"
        
        return Response({
            "response": respuesta_texto,
            "timestamp": timezone.now().isoformat()
        })
        
    except req.exceptions.Timeout:
        print("Error: Timeout al conectar con Gemini API")
        return Response(
            {"message": "El servicio de IA está tardando demasiado. Intenta con una pregunta más simple."},
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except Exception as e:
        import traceback
        print("Error en chatbot:", str(e))
        print(traceback.format_exc())
        return Response(
            {"message": "Lo siento, no puedo conectarme con el servicio de IA en este momento."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
