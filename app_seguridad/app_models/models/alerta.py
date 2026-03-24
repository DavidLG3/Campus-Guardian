"""alerta.py module: backend logic for Campus Guardian."""
from django.db import models
from .usuario import Usuario
from .incidencia import Incidencia

class Alerta(models.Model):
    """Alert sent to users about incidents that need attention."""

    # Simple status values for tracking alert life cycle
    ESTADOS_ALERTA = (
        ('pendiente', 'Pendiente'),
        ('leida', 'Leída'),
        ('resuelta', 'Resuelta'),
    )

    # Incident this alert is about
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    # User who should see this alert (usually security staff)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    # Main message explaining what the alert is for
    mensaje = models.TextField()
    # When the alert was created (set automatically)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Current status of the alert
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_ALERTA,
        default='pendiente'
    )

    def __str__(self):
        # String representation showing user and alert status
        return f"Alerta para {self.usuario.username} - {self.estado}"
