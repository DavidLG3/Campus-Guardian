"""crear_admin.py module: backend logic for Campus Guardian."""
from django.core.management.base import BaseCommand
from app_models.models import Usuario

class Command(BaseCommand):
    help = 'Crea el usuario administrador predeterminado'

    def handle(self, *args, **kwargs):
        # Verificar si ya existe el administrador por username o email
        if Usuario.objects.filter(username='admin').exists():
            # Si existe, actualizar su tipo a admin
            admin = Usuario.objects.get(username='admin')
            admin.tipo = 'admin'
            admin.email = 'admin@email.com'
            admin.set_password('admin123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.first_name = 'Administrador'
            admin.last_name = 'Sistema'
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario administrador actualizado: {admin.email}'))
            return

        # Crear el usuario administrador
        admin = Usuario.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='admin123',
            tipo='admin',
            first_name='Administrador',
            last_name='Sistema',
            is_staff=True,
            is_superuser=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Usuario administrador creado exitosamente: {admin.email}'))
