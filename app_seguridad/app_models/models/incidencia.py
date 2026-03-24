"""incidencia.py module: backend logic for Campus Guardian."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from .usuario import Usuario

class Incidencia(models.Model):
    TIPOS_INCIDENCIA = (
        ('robo', 'Robo'),
        ('accidente', 'Accidente'),
        ('incendio', 'Incendio'),
        ('vandalismo', 'Vandalismo'),
        ('situacion_incomoda', 'Situación Incómoda'),
        ('estafa', 'Estafa'),
        ('otro', 'Otro'),
    )

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
    )

    # Unique incident tracking code (auto-generated on save)
    codigo_unico = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Código único de la incidencia (ej: INC-2024-0001)"
    )
    
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_INCIDENCIA)
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    # User who reported the incident
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="incidencias"
    )

    # Location fields used by the Leaflet map
    # Geographic coordinates (required for the map)
    latitud = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        default=0.0,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ],
        help_text="Latitud de la incidencia (entre -90 y 90)"
    )
    longitud = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        default=0.0,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ],
        help_text="Longitud de la incidencia (entre -180 y 180)"
    )
    
    # Human-friendly address (optional but useful)
    direccion = models.CharField(
        max_length=300,
        blank=True,
        default='',
        help_text="Dirección o descripción del lugar (ej: 'Biblioteca Central, 2do piso')"
    )

    # Current incident status
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )
    
    # Assigned user (security staff handling the incident)
    asignado_a = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incidencias_asignadas",
        help_text="Usuario de seguridad asignado a esta incidencia"
    )
    
    # Resolution note (written by security staff)
    nota_resolucion = models.TextField(
        blank=True,
        default='',
        help_text="Nota del personal de seguridad al resolver la incidencia"
    )
    fecha_resolucion = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se resolvió la incidencia"
    )
    resuelto_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incidencias_resueltas",
        help_text="Usuario de seguridad que resolvió la incidencia"
    )

    def __str__(self):
        return f"[{self.codigo_unico}] {self.titulo} - {self.estado}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_unico:
            # Generate unique code: INC-YYYY-NNNN
            year = datetime.now().year
            # Get the last incident number from the current year
            last_incidencia = Incidencia.objects.filter(
                codigo_unico__startswith=f'INC-{year}-'
            ).order_by('codigo_unico').last()
            
            if last_incidencia:
                # Extract the number and increment it
                last_number = int(last_incidencia.codigo_unico.split('-')[-1])
                new_number = last_number + 1
            else:
                # First incident of the year
                new_number = 1
            
            self.codigo_unico = f'INC-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)
