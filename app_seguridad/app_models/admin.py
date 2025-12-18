from django.contrib import admin
from .models import Usuario
from .models import Alerta
from .models import Incidencia
from .models import Notificacion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "tipo", "is_staff", "is_active")
    list_filter = ("tipo", "is_staff", "is_active")
    search_fields = ("username", "email")

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ("codigo_unico", "tipo", "estado", "fecha_reporte", "usuario", "latitud", "longitud")
    list_filter = ("tipo", "estado", "fecha_reporte")
    search_fields = ("codigo_unico", "descripcion")

@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    list_display = ("incidencia", "usuario", "estado", "fecha_creacion")
    list_filter = ("estado", "fecha_creacion")
    search_fields = ("mensaje",)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "incidencia", "tipo", "leida", "fecha_creacion")
    list_filter = ("tipo", "leida", "fecha_creacion")
    search_fields = ("mensaje", "usuario__username")