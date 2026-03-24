"""comentario.py module: backend logic for Campus Guardian."""
from django.db import models
from .incidencia import Incidencia
from .usuario import Usuario


class Comentario(models.Model):
    """Stores user comments attached to incidents."""
    
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    
    contenido = models.TextField(
        help_text="Contenido del comentario"
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.usuario.first_name or self.usuario.username} - {self.incidencia.codigo_unico}"
