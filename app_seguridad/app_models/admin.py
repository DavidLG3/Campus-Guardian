"""admin.py module: backend logic for Campus Guardian."""
from django.contrib import admin
from .models import Usuario
from .models import Alerta
from .models import Incidencia
from .models import Notificacion
from .models import ArchivoIncidencia
from .models import Comentario

# User management admin interface
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "tipo", "is_staff", "is_active")
    list_filter = ("tipo", "is_staff", "is_active")
    search_fields = ("username", "email")

# Incident management and tracking admin interface
@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ("codigo_unico", "tipo", "estado", "fecha_reporte", "usuario", "latitud", "longitud")
    list_filter = ("tipo", "estado", "fecha_reporte")
    search_fields = ("codigo_unico", "descripcion")

# Alert notifications admin interface
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("incidencia", "usuario", "estado", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("mensaje",)

# User notification admin interface
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "incidencia", "tipo", "leida", "fecha_creacion")
    list_filter = ("tipo", "leida", "fecha_creacion")
    search_fields = ("mensaje", "usuario__username")

# Incident files (photos/videos) admin interface
@admin.register(ArchivoIncidencia)
class ArchivoIncidenciaAdmin(admin.ModelAdmin):
    list_display = ("incidencia", "tipo", "archivo", "fecha_subida")
    list_filter = ("tipo", "fecha_subida")
    search_fields = ("incidencia__codigo_unico", "descripcion")

# Incident comments admin interface
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "incidencia", "contenido_corto", "fecha_creacion")
    list_filter = ("fecha_creacion",)
    search_fields = ("contenido", "usuario__username", "incidencia__codigo_unico")
    
    # Display truncated comment content in list view
    def contenido_corto(self, obj):
        return obj.contenido[:50] + "..." if len(obj.contenido) > 50 else obj.contenido
    contenido_corto.short_description = "Contenido"
