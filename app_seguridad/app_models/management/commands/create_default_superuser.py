"""create_default_superuser.py module: backend logic for Campus Guardian."""
from django.core.management.base import BaseCommand
from app_models.models import Usuario


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        admin_user, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@campusguardian.com',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'tipo': 'admin',
                'rol': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        if created:
            admin_user.set_password('admin123')
            admin_user.save(update_fields=['password'])
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
            return

        admin_user.tipo = 'admin'
        admin_user.rol = 'admin'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save(update_fields=['tipo', 'rol', 'is_staff', 'is_superuser'])
        self.stdout.write(self.style.SUCCESS('Superusuario actualizado como tipo admin'))
