"""signals.py module: backend logic for Campus Guardian."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Incidencia, Usuario, Alerta, Notificacion

# Temporary storage for previous incident state
_estado_anterior = {}

@receiver(pre_save, sender=Incidencia)
def guardar_estado_anterior(sender, instance, **kwargs):
    """Store the previous state before updating the incident."""
    if instance.pk:
        try:
            incidencia_anterior = Incidencia.objects.get(pk=instance.pk)
            _estado_anterior[instance.pk] = incidencia_anterior.estado
        except Incidencia.DoesNotExist:
            _estado_anterior[instance.pk] = None

@receiver(post_save, sender=Incidencia)
def crear_alertas_y_notificaciones(sender, instance, created, **kwargs):
    if created:
        # Create alerts for security staff when a new incident is created
        usuarios_seguridad = Usuario.objects.filter(tipo="seguridad")
        descripcion_corta = instance.descripcion[:50] + '...' if len(instance.descripcion) > 50 else instance.descripcion
        for usuario in usuarios_seguridad:
            Alerta.objects.create(
                incidencia=instance,
                usuario=usuario,
                mensaje=f"Nueva incidencia {instance.codigo_unico}: {descripcion_corta}"
            )
    else:
        # Detect state changes to create notifications to the citizen
        estado_anterior = _estado_anterior.get(instance.pk)
        
        print(f"[SIGNAL] Estado anterior: {estado_anterior}, Estado nuevo: {instance.estado}")
        print(f"[SIGNAL] Usuario de la incidencia: {instance.usuario}")
        
        # Check that the incident has an assigned user
        if not instance.usuario:
            print("[SIGNAL] No hay usuario asignado a la incidencia, saltando notificación")
            if instance.pk in _estado_anterior:
                del _estado_anterior[instance.pk]
            return
        
        # If state changed to 'en_proceso' (in progress)
        if instance.estado == 'en_proceso' and estado_anterior != 'en_proceso':
            nombre_operador = instance.asignado_a.first_name or instance.asignado_a.username if instance.asignado_a else "Personal de seguridad"
            notificacion = Notificacion.objects.create(
                usuario=instance.usuario,
                incidencia=instance,
                tipo='en_progreso',
                mensaje=f"Tu incidencia {instance.codigo_unico} está siendo atendida. {nombre_operador} va de camino."
            )
            print(f"[SIGNAL] Notificación 'en_progreso' creada: {notificacion.id} - {notificacion.mensaje}")
        
        # If state changed to 'resuelta' (resolved)
        elif instance.estado == 'resuelta' and estado_anterior != 'resuelta':
            notificacion = Notificacion.objects.create(
                usuario=instance.usuario,
                incidencia=instance,
                tipo='resuelta',
                mensaje=f"Tu incidencia {instance.codigo_unico} ha sido resuelta."
            )
            print(f"[SIGNAL] Notificación 'resuelta' creada: {notificacion.id} - {notificacion.mensaje}")
            # Mark all alerts as read
            Alerta.objects.filter(incidencia=instance).update(estado='leida')
        
        # Clean up the previous state
        if instance.pk in _estado_anterior:
            del _estado_anterior[instance.pk]
