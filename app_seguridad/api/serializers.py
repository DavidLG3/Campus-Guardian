"""Serializers used by the Campus Guardian API endpoints."""
from rest_framework import serializers
from app_models.models import Usuario, Incidencia, Alerta, Notificacion, ArchivoIncidencia, Comentario


class UsuarioSerializer(serializers.ModelSerializer):
    """User serializer with profile fields and password handling."""
    password = serializers.CharField(write_only=True, required=False)
    nombre = serializers.CharField(source='first_name', required=False)
    telefono = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    foto_perfil = serializers.ImageField(required=False, allow_null=True)
    foto_perfil_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo', 'rol', 
                  'nombre', 'first_name', 'last_name', 'telefono', 'foto_perfil', 
                  'foto_perfil_url', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'username', 'foto_perfil_url']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': True}
        }
    
    def get_foto_perfil_url(self, obj):
        """Build the full avatar URL when a profile image exists."""
        if obj.foto_perfil:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_perfil.url)
            return obj.foto_perfil.url
        return None
    
    def validate_email(self, value):
        """Ensure the email is unique, including during profile updates."""
        instance = self.instance
        if instance:
            # During updates, ignore the current user.
            if Usuario.objects.exclude(pk=instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("Ya existe un usuario con ese correo electrónico")
        else:
            # During creation, the email must not exist yet.
            if Usuario.objects.filter(email=value).exists():
                raise serializers.ValidationError("Ya existe un usuario con ese correo electrónico")
        return value
    
    def validate_password(self, value):
        """Prevent users from reusing their current password."""
        instance = self.instance
        if instance and value:
            # Reject the new password if it matches the current one.
            if instance.check_password(value):
                raise serializers.ValidationError("La nueva contraseña debe ser diferente a la anterior")
        return value
    
    def create(self, validated_data):
        """Create a user and store the password securely."""
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """Update a user and hash the password when provided."""
        password = validated_data.pop('password', None)
        
        # Map the API-facing `nombre` field to Django's `first_name`.
        if 'first_name' in validated_data:
            instance.first_name = validated_data.pop('first_name')
        
        # Keep the current active flag unless it is explicitly provided.
        if 'is_active' not in validated_data:
            validated_data['is_active'] = instance.is_active
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        """Expose `nombre` in responses as a friendly alias for `first_name`."""
        representation = super().to_representation(instance)
        representation['nombre'] = instance.first_name
        return representation


class ArchivoIncidenciaSerializer(serializers.ModelSerializer):
    """Serializer for files attached to incidents."""
    archivo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ArchivoIncidencia
        fields = ['id', 'archivo', 'archivo_url', 'tipo', 'descripcion', 'fecha_subida']
        read_only_fields = ['id', 'fecha_subida']
    
    def get_archivo_url(self, obj):
        """Return the full file URL from Cloudinary."""
        return obj.get_cloudinary_url()


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer for incident comments."""
    usuario_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Comentario
        fields = ['id', 'incidencia', 'usuario', 'usuario_info', 'contenido', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion', 'usuario', 'usuario_info']
    
    def get_usuario_info(self, obj):
        foto_url = None
        if obj.usuario.foto_perfil:
            request = self.context.get('request')
            if request:
                foto_url = request.build_absolute_uri(obj.usuario.foto_perfil.url)
        
        return {
            'id': obj.usuario.id,
            'nombre': obj.usuario.first_name or obj.usuario.username,
            'username': obj.usuario.username,
            'tipo': obj.usuario.tipo,
            'foto_perfil_url': foto_url
        }


class IncidenciaSerializer(serializers.ModelSerializer):
    """Main serializer for incident details returned to the frontend."""
    usuario_reporta = serializers.SerializerMethodField()
    usuario_asignado = serializers.SerializerMethodField()
    resuelto_por_nombre = serializers.SerializerMethodField()
    fecha_creacion = serializers.DateTimeField(source='fecha_reporte', read_only=True)
    estado = serializers.SerializerMethodField()
    archivos = ArchivoIncidenciaSerializer(many=True, read_only=True)
    comentarios = ComentarioSerializer(many=True, read_only=True)
    comentarios_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Incidencia
        fields = ['id', 'codigo_unico', 'descripcion', 'tipo', 'fecha_creacion', 'fecha_reporte',
                  'usuario', 'usuario_reporta', 'usuario_asignado', 'asignado_a', 'latitud', 'longitud', 
                  'direccion', 'estado', 'nota_resolucion', 'fecha_resolucion', 
                  'resuelto_por', 'resuelto_por_nombre', 'archivos', 'comentarios', 'comentarios_count']
        read_only_fields = ['id', 'codigo_unico', 'fecha_reporte', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_reporte', 'fecha_creacion']
    
    def get_usuario_reporta(self, obj):
        return {
            'nombre': obj.usuario.first_name or obj.usuario.username,
            'email': obj.usuario.email
        }
    
    def get_usuario_asignado(self, obj):
        if obj.asignado_a:
            return {
                'id': obj.asignado_a.id,
                'nombre': obj.asignado_a.first_name or obj.asignado_a.username,
                'email': obj.asignado_a.email
            }
        return None
    
    def get_resuelto_por_nombre(self, obj):
        if obj.resuelto_por:
            return {
                'nombre': obj.resuelto_por.first_name or obj.resuelto_por.username,
                'email': obj.resuelto_por.email
            }
        return None
    
    def get_estado(self, obj):
        # Translate backend status values to the names used by the frontend.
        estado_map = {
            'pendiente': 'abierta',
            'en_proceso': 'en_progreso',
            'resuelta': 'resuelta'
        }
        return estado_map.get(obj.estado, obj.estado)
    
    def get_comentarios_count(self, obj):
        return obj.comentarios.count()


class IncidenciaCreateSerializer(serializers.ModelSerializer):
    """Serializer used when creating incidents from client requests."""
    
    class Meta:
        model = Incidencia
        fields = ['id', 'descripcion', 'tipo', 'latitud', 'longitud', 'direccion']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # New incidents start as pending by default.
        validated_data['estado'] = 'pendiente'
        return super().create(validated_data)
        return incidencia


class AlertaSerializer(serializers.ModelSerializer):
    """Serializer for system alerts and alert metadata."""
    fecha_creacion = serializers.DateTimeField(read_only=True)
    leida = serializers.SerializerMethodField()
    activa = serializers.BooleanField(default=True, write_only=True, required=False)
    
    # Extra frontend-facing fields not stored directly in the model.
    tipo = serializers.CharField(required=False, allow_blank=True, write_only=True)
    nivel = serializers.CharField(required=False, allow_blank=True, write_only=True)
    ubicacion = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    # Allow creating alerts without linking an incident explicitly.
    incidencia = serializers.PrimaryKeyRelatedField(
        queryset=Incidencia.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Alerta
        fields = ['id', 'incidencia', 'usuario', 'mensaje', 'fecha_creacion', 
                  'estado', 'leida', 'activa', 'tipo', 'nivel', 'ubicacion']
        read_only_fields = ['id', 'fecha_creacion', 'leida', 'usuario']
    
    def get_leida(self, obj):
        return obj.estado == 'leida'
    
    def to_representation(self, instance):
        """Shape the response with the extra fields expected by the frontend."""
        data = super().to_representation(instance)
        # Derive display fields from the related incident when available.
        if instance.incidencia:
            data['tipo'] = 'Nueva Incidencia'
            data['nivel'] = instance.incidencia.prioridad if hasattr(instance.incidencia, 'prioridad') else 'medio'
            data['ubicacion'] = instance.incidencia.direccion if instance.incidencia.direccion else f"Lat: {instance.incidencia.latitud}, Lng: {instance.incidencia.longitud}"
        else:
            data['tipo'] = 'Notificación'
            data['nivel'] = 'medio'
            data['ubicacion'] = ''
        data['activa'] = instance.estado != 'resuelta'
        return data
    
    def create(self, validated_data):
        # Remove request-only fields that do not belong to the model.
        tipo = validated_data.pop('tipo', None)
        nivel = validated_data.pop('nivel', None)
        ubicacion = validated_data.pop('ubicacion', None)
        validated_data.pop('activa', None)
        
        # If no incident is provided, create a generic one to keep the relation.
        if 'incidencia' not in validated_data or validated_data.get('incidencia') is None:
            # Create a fallback incident for system-generated alerts.
            incidencia = Incidencia.objects.create(
                titulo=f"Alerta: {tipo or 'General'}",
                descripcion=validated_data.get('mensaje', 'Alerta del sistema'),
                tipo='otro',
                usuario=validated_data.get('usuario'),
                estado='pendiente',
                latitud=0.0,
                longitud=0.0
            )
            validated_data['incidencia'] = incidencia
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Allow toggling `leida` by mapping it to the internal status value.
        if 'leida' in validated_data:
            leida = validated_data.pop('leida')
            instance.estado = 'leida' if leida else 'pendiente'
        
        # Drop request-only fields before model update.
        validated_data.pop('tipo', None)
        validated_data.pop('nivel', None)
        validated_data.pop('ubicacion', None)
        validated_data.pop('activa', None)
        
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer used to validate and create new user accounts."""
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    nombre = serializers.CharField(write_only=True, required=True, max_length=100)
    telefono = serializers.CharField(required=False, allow_blank=True, max_length=20)
    rol = serializers.ChoiceField(
        choices=['ciudadano', 'operador'],
        required=False,
        default='ciudadano',
        write_only=True
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'rol', 'password']
    
    def validate_email(self, value):
        """Validate UAM email format with allowed institutional domains."""
        import re
        
        # Must contain exactly one @ symbol.
        if value.count('@') != 1:
            raise serializers.ValidationError("El email debe contener exactamente un símbolo @")
        
        # Normalize before applying format checks.
        value = value.lower().strip()
        
        # Only allow official UAM domains.
        if not (value.endswith('@uam.es') or value.endswith('@estudiante.uam.es')):
            raise serializers.ValidationError(
                "Solo se permiten correos institucionales de la UAM (@uam.es o @estudiante.uam.es)"
            )
        
        # Keep within RFC-safe max length.
        if len(value) > 254:
            raise serializers.ValidationError("El email es demasiado largo (máximo 254 caracteres)")
        
        # Ensure the local-part exists.
        parte_local = value.split('@')[0]
        if not parte_local or len(parte_local) < 1:
            raise serializers.ValidationError("El email no tiene una parte válida antes del @")
        
        # Restrict local-part characters for consistency.
        if not re.match(r'^[a-z0-9._-]+$', parte_local):
            raise serializers.ValidationError(
                "El email solo puede contener letras, números, puntos, guiones y guiones bajos antes del @"
            )
        
        # Email must be unique.
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        
        return value
    
    def validate_telefono(self, value):
        """Validate phone format as international prefix plus 9 digits."""
        import re
        
        if not value or value.strip() == '':
            return ''
        
        # Expected format: +XX123456789 or +XXX123456789.
        value = value.strip()
        
        # Prefix must start with +.
        if not value.startswith('+'):
            raise serializers.ValidationError("El teléfono debe incluir el prefijo internacional")
        
        # Split prefix and local number.
        match = re.match(r'^(\+\d{1,3})(\d{9})$', value)
        if not match:
            raise serializers.ValidationError(
                "El teléfono debe tener un prefijo válido (+XX) seguido de exactamente 9 dígitos"
            )
        
        prefijo, numero = match.groups()
        
        # Enforce fixed local length.
        if len(numero) != 9:
            raise serializers.ValidationError("El número debe tener exactamente 9 dígitos (sin contar el prefijo)")
        
        return value
    
    def validate_nombre(self, value):
        """Validate name length and accepted characters."""
        value = value.strip()
        
        if len(value) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        
        if len(value) > 100:
            raise serializers.ValidationError("El nombre es demasiado largo (máximo 100 caracteres)")
        
        # Allow letters, spaces, hyphens, and apostrophes.
        import re
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-']+$", value):
            raise serializers.ValidationError("El nombre solo puede contener letras, espacios, guiones y apóstrofes")
        
        return value
    
    def validate_password(self, value):
        """Validate a strong password using basic security requirements."""
        import re
        
        # Minimum and maximum length.
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if len(value) > 128:
            raise serializers.ValidationError("La contraseña es demasiado larga (máximo 128 caracteres)")
        
        # Require at least one lowercase letter.
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula")
        
        # Require at least one uppercase letter.
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula")
        
        # Require at least one number.
        if not re.search(r'\d', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número")
        
        # Require at least one special character.
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;/]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial (!@#$%^&*...)")
        
        # Do not allow spaces.
        if ' ' in value:
            raise serializers.ValidationError("La contraseña no puede contener espacios")
        
        return value
    
    def create(self, validated_data):
        """Create a new user from validated registration data."""
        nombre = validated_data.pop('nombre')
        telefono = validated_data.pop('telefono', '')
        rol = validated_data.pop('rol', 'ciudadano')
        password = validated_data.pop('password')
        email = validated_data.get('email')
        
        # Build a username from the email local-part.
        username = email.split('@')[0]
        
        # If needed, append a numeric suffix to keep it unique.
        base_username = username
        counter = 1
        while Usuario.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Map UI role to internal user type.
        tipo = 'seguridad' if rol == 'operador' else 'normal'
        
        # Create and persist the user.
        usuario = Usuario(
            username=username,
            email=email,
            first_name=nombre,
            tipo=tipo,
            rol=rol
        )
        
        # Temporary workaround: store phone in last_name when provided.
        # Ideally, `telefono` should exist as a proper model field.
        if telefono:
            usuario.last_name = telefono
        
        usuario.set_password(password)
        usuario.save()
        return usuario


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer for citizen-facing notifications."""
    incidencia_codigo = serializers.SerializerMethodField()
    
    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'incidencia', 'incidencia_codigo', 'tipo', 
                  'mensaje', 'leida', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_incidencia_codigo(self, obj):
        """Return the incident code when linked, otherwise None."""
        return obj.incidencia.codigo_unico if obj.incidencia else None
