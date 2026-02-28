from django.core.management.base import BaseCommand
from app_models.models import Usuario

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para Cypress tests'

    def handle(self, *args, **kwargs):
        usuarios_test = [
            {
                'username': 'test_admin',
                'email': 'test_admin@uam.es',
                'password': 'Admin123!',
                'first_name': 'Admin Test',
                'tipo': 'admin',
                'rol': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'test_operador',
                'email': 'test_operador@uam.es',
                'password': 'Operador123!',
                'first_name': 'Operador Test',
                'tipo': 'seguridad',
                'rol': 'operador',
                'is_staff': False,
                'is_superuser': False
            },
            {
                'username': 'test_ciudadano',
                'email': 'test_ciudadano@estudiante.uam.es',
                'password': 'Ciudadano123!',
                'first_name': 'Ciudadano Test',
                'tipo': 'normal',
                'rol': 'ciudadano',
                'is_staff': False,
                'is_superuser': False
            }
        ]

        for user_data in usuarios_test:
            username = user_data['username']
            
            # Verificar si ya existe
            if Usuario.objects.filter(username=username).exists():
                # Actualizar usuario existente
                usuario = Usuario.objects.get(username=username)
                usuario.email = user_data['email']
                usuario.set_password(user_data['password'])
                usuario.first_name = user_data['first_name']
                usuario.tipo = user_data['tipo']
                usuario.rol = user_data['rol']
                usuario.is_staff = user_data['is_staff']
                usuario.is_superuser = user_data['is_superuser']
                usuario.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Usuario {username} actualizado: {usuario.email} (tipo: {usuario.tipo}, rol: {usuario.rol})')
                )
            else:
                # Crear nuevo usuario
                usuario = Usuario.objects.create_user(
                    username=username,
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    tipo=user_data['tipo'],
                    rol=user_data['rol'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser']
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Usuario {username} creado: {usuario.email} (tipo: {usuario.tipo}, rol: {usuario.rol})')
                )

        self.stdout.write(self.style.SUCCESS('\n¡Usuarios de prueba listos para Cypress!'))
