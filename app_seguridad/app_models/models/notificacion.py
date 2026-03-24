"""notificacion.py module: backend logic for Campus Guardian."""
from django.db import models
from .usuario import Usuario
from .incidencia import Incidencia


class Notificacion(models.Model):
    """
    Modelo para notificaciones a ciudadanos sobre el estado de sus incidencias
    """
    TIPOS = (
        ('en_progreso', 'Incidencia en Progreso'),
        ('resuelta', 'Incidencia Resuelta'),
    )
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Ciudadano que recibe la notificación"
    )
    
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name='notificaciones',
        help_text="Incidencia relacionada con la notificación"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        help_text="Tipo de notificación"
    )
    
    mensaje = models.TextField(
        help_text="Mensaje de la notificación"
    )
    
    leida = models.BooleanField(
        default=False,
        help_text="Si la notificación ha sido leída"
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la notificación"
    )
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.tipo}"
