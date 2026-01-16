from django.db import models
from .incidencia import Incidencia


class ArchivoIncidencia(models.Model):
    """Modelo para almacenar fotos y videos adjuntos a una incidencia"""
    
    TIPOS_ARCHIVO = (
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    )
    
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name='archivos'
    )
    
    archivo = models.FileField(
        upload_to='incidencias/%Y/%m/',
        help_text="Archivo de imagen o video"
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_ARCHIVO,
        help_text="Tipo de archivo: imagen o video"
    )
    
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    # Metadatos opcionales
    descripcion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Descripción opcional del archivo"
    )
    
    class Meta:
        verbose_name = "Archivo de Incidencia"
        verbose_name_plural = "Archivos de Incidencias"
        ordering = ['fecha_subida']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.incidencia.codigo_unico}"
