"""signals.py module: backend logic for Campus Guardian."""
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Incidencia, Usuario, Alerta, Notificacion, ArchivoIncidencia
import cloudinary.uploader

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


@receiver(pre_save, sender=Usuario)
def eliminar_avatar_anterior_en_cambio(sender, instance, **kwargs):
    """Delete old profile photo from storage when user uploads a new one."""
    if not instance.pk:
        return

    try:
        usuario_anterior = Usuario.objects.get(pk=instance.pk)
    except Usuario.DoesNotExist:
        return

    foto_anterior = usuario_anterior.foto_perfil
    foto_nueva = instance.foto_perfil

    # If avatar changed, remove previous file from storage (Cloudinary in prod).
    if foto_anterior and foto_anterior != foto_nueva:
        foto_anterior.delete(save=False)


@receiver(post_delete, sender=Usuario)
def eliminar_avatar_al_borrar_usuario(sender, instance, **kwargs):
    """Delete user profile photo from storage when the user is deleted."""
    if instance.foto_perfil:
        instance.foto_perfil.delete(save=False)


@receiver(post_delete, sender=ArchivoIncidencia)
def eliminar_archivo_cloudinary_al_borrar(sender, instance, **kwargs):
    """Delete Cloudinary asset when an incident attachment is removed."""
    if not instance.cloudinary_public_id:
        return

    resource_type = 'video' if instance.tipo == 'video' else 'image'

    try:
        cloudinary.uploader.destroy(
            instance.cloudinary_public_id,
            resource_type=resource_type,
            invalidate=True,
        )
    except Exception as exc:
        # Keep DB deletion flow resilient even if external provider fails.
        print(f"[CLOUDINARY] Error eliminando recurso {instance.cloudinary_public_id}: {exc}")
