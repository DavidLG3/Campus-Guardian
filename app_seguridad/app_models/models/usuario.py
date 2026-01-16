from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('normal', 'Usuario Normal'),
        ('seguridad', 'Usuario de Seguridad'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='normal')
    
    # Campo adicional para usuarios normales
    rol = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Rol del usuario dentro de la Universidad (ej: Estudiante, Profesor, Personal Administrativo)"
    )
    
    # Información de contacto
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de teléfono del usuario"
    )
    
    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Foto de perfil del usuario"
    )

    def __str__(self):
        return f"{self.username} ({self.tipo})"
