"""alerta.py module: backend logic for Campus Guardian."""
from django.db import models
from .usuario import Usuario
from .incidencia import Incidencia

class Alerta(models.Model):
    ESTADOS_ALERTA = (
        ('pendiente', 'Pendiente'),
        ('leida', 'Leída'),
        ('resuelta', 'Resuelta'),
    )

    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_ALERTA,
        default='pendiente'
    )

    def __str__(self):
        return f"Alerta para {self.usuario.username} - {self.estado}"
