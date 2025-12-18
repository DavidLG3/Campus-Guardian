from rest_framework import serializers
from app_models.models import Usuario, Incidencia, Alerta, Notificacion


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'tipo', 'rol', 
                  'first_name', 'last_name', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        password = validated_data.pop('password', None)
        usuario = Usuario(**validated_data)
        if password:
            usuario.set_password(password)
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        """Actualizar usuario, encriptando contraseña si se proporciona"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class IncidenciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Incidencia"""
    usuario_reporta = serializers.SerializerMethodField()
    usuario_asignado = serializers.SerializerMethodField()
    resuelto_por_nombre = serializers.SerializerMethodField()
    fecha_creacion = serializers.DateTimeField(source='fecha_reporte', read_only=True)
    estado = serializers.SerializerMethodField()
    
    class Meta:
        model = Incidencia
        fields = ['id', 'codigo_unico', 'descripcion', 'tipo', 'fecha_creacion', 'fecha_reporte',
                  'usuario', 'usuario_reporta', 'usuario_asignado', 'asignado_a', 'latitud', 'longitud', 
                  'direccion', 'estado', 'nota_resolucion', 'fecha_resolucion', 
                  'resuelto_por', 'resuelto_por_nombre']
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
        # Mapear estados del modelo a los que espera el frontend
        estado_map = {
            'pendiente': 'abierta',
            'en_proceso': 'en_progreso',
            'resuelta': 'resuelta'
        }
        return estado_map.get(obj.estado, obj.estado)


class IncidenciaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear incidencias (sin especificar usuario manualmente)"""
    
    class Meta:
        model = Incidencia
        fields = ['id', 'descripcion', 'tipo', 'latitud', 'longitud', 'direccion']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        # Por defecto, estado pendiente
        validated_data['estado'] = 'pendiente'
        return super().create(validated_data)


class AlertaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Alerta"""
    fecha_creacion = serializers.DateTimeField(read_only=True)
    leida = serializers.SerializerMethodField()
    activa = serializers.BooleanField(default=True, write_only=True, required=False)
    
    # Campos adicionales que espera el frontend
    tipo = serializers.CharField(required=False, allow_blank=True, write_only=True)
    nivel = serializers.CharField(required=False, allow_blank=True, write_only=True)
    ubicacion = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    # Hacer incidencia opcional
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
        """Personalizar la salida para incluir campos que espera el frontend"""
        data = super().to_representation(instance)
        # Agregar campos basados en la incidencia relacionada
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
        # Extraer campos que no están en el modelo
        tipo = validated_data.pop('tipo', None)
        nivel = validated_data.pop('nivel', None)
        ubicacion = validated_data.pop('ubicacion', None)
        validated_data.pop('activa', None)
        
        # Si no se proporciona incidencia, crear una automática
        if 'incidencia' not in validated_data or validated_data.get('incidencia') is None:
            # Crear una incidencia genérica para la alerta
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
        # Manejar el campo leida
        if 'leida' in validated_data:
            leida = validated_data.pop('leida')
            instance.estado = 'leida' if leida else 'pendiente'
        
        # Extraer campos que no están en el modelo
        validated_data.pop('tipo', None)
        validated_data.pop('nivel', None)
        validated_data.pop('ubicacion', None)
        validated_data.pop('activa', None)
        
        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    password = serializers.CharField(write_only=True, min_length=6)
    nombre = serializers.CharField(write_only=True, required=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    rol = serializers.ChoiceField(
        choices=['ciudadano', 'operador'],
        required=True,
        write_only=True
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'rol', 'password']
    
    def validate_email(self, value):
        """Validar que el email no esté ya registrado"""
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado")
        return value
    
    def create(self, validated_data):
        """Crear usuario registrado"""
        nombre = validated_data.pop('nombre')
        telefono = validated_data.pop('telefono', '')
        rol = validated_data.pop('rol', 'ciudadano')
        password = validated_data.pop('password')
        email = validated_data.get('email')
        
        # Crear username a partir del email
        username = email.split('@')[0]
        
        # Si el username ya existe, agregar un número
        base_username = username
        counter = 1
        while Usuario.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Determinar el tipo según el rol
        tipo = 'seguridad' if rol == 'operador' else 'normal'
        
        # Crear el usuario
        usuario = Usuario(
            username=username,
            email=email,
            first_name=nombre,
            tipo=tipo,
            rol=rol
        )
        
        # Si se proporcionó teléfono, guardarlo en last_name (temporal)
        # Idealmente deberías agregar un campo telefono al modelo Usuario
        if telefono:
            usuario.last_name = telefono
        
        usuario.set_password(password)
        usuario.save()
        return usuario


class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones de ciudadanos"""
    incidencia_codigo = serializers.SerializerMethodField()
    
    class Meta:
        model = Notificacion
        fields = ['id', 'usuario', 'incidencia', 'incidencia_codigo', 'tipo', 
                  'mensaje', 'leida', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_incidencia_codigo(self, obj):
        """Retorna el código de incidencia si existe, sino None"""
        return obj.incidencia.codigo_unico if obj.incidencia else None
