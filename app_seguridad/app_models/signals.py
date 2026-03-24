"""signals.py module: backend logic for Campus Guardian."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Incidencia, Usuario, Alerta, Notificacion

# Variable temporal para guardar el estado anterior
_estado_anterior = {}

@receiver(pre_save, sender=Incidencia)
def guardar_estado_anterior(sender, instance, **kwargs):
    """Guardar el estado anterior antes de actualizar"""
    if instance.pk:
        try:
            incidencia_anterior = Incidencia.objects.get(pk=instance.pk)
            _estado_anterior[instance.pk] = incidencia_anterior.estado
        except Incidencia.DoesNotExist:
            _estado_anterior[instance.pk] = None

@receiver(post_save, sender=Incidencia)
def crear_alertas_y_notificaciones(sender, instance, created, **kwargs):
    if created:
        # Crear alertas para usuarios de seguridad cuando se crea nueva incidencia
        usuarios_seguridad = Usuario.objects.filter(tipo="seguridad")
        descripcion_corta = instance.descripcion[:50] + '...' if len(instance.descripcion) > 50 else instance.descripcion
        for usuario in usuarios_seguridad:
            Alerta.objects.create(
                incidencia=instance,
                usuario=usuario,
                mensaje=f"Nueva incidencia {instance.codigo_unico}: {descripcion_corta}"
            )
    else:
        # Detectar cambios de estado para crear notificaciones al ciudadano
        estado_anterior = _estado_anterior.get(instance.pk)
        
        print(f"[SIGNAL] Estado anterior: {estado_anterior}, Estado nuevo: {instance.estado}")
        print(f"[SIGNAL] Usuario de la incidencia: {instance.usuario}")
        
        # Verificar que la incidencia tenga un usuario asignado
        if not instance.usuario:
            print("[SIGNAL] No hay usuario asignado a la incidencia, saltando notificación")
            if instance.pk in _estado_anterior:
                del _estado_anterior[instance.pk]
            return
        
        # Si cambió a "en_proceso" (en progreso)
        if instance.estado == 'en_proceso' and estado_anterior != 'en_proceso':
            nombre_operador = instance.asignado_a.first_name or instance.asignado_a.username if instance.asignado_a else "Personal de seguridad"
            notificacion = Notificacion.objects.create(
                usuario=instance.usuario,
                incidencia=instance,
                tipo='en_progreso',
                mensaje=f"Tu incidencia {instance.codigo_unico} está siendo atendida. {nombre_operador} va de camino."
            )
            print(f"[SIGNAL] Notificación 'en_progreso' creada: {notificacion.id} - {notificacion.mensaje}")
        
        # Si cambió a "resuelta"
        elif instance.estado == 'resuelta' and estado_anterior != 'resuelta':
            notificacion = Notificacion.objects.create(
                usuario=instance.usuario,
                incidencia=instance,
                tipo='resuelta',
                mensaje=f"Tu incidencia {instance.codigo_unico} ha sido resuelta."
            )
            print(f"[SIGNAL] Notificación 'resuelta' creada: {notificacion.id} - {notificacion.mensaje}")
            # Marcar todas las alertas como leídas
            Alerta.objects.filter(incidencia=instance).update(estado='leida')
        
        # Limpiar el estado anterior
        if instance.pk in _estado_anterior:
            del _estado_anterior[instance.pk]
