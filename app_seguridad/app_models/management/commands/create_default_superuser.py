from django.core.management.base import BaseCommand
from app_models.models import Usuario


class Command(BaseCommand):
    help = 'Crea un superusuario si no existe'

    def handle(self, *args, **options):
        if not Usuario.objects.filter(username='admin').exists():
            Usuario.objects.create_superuser(
                username='admin',
                email='admin@campusguardian.com',
                password='admin123',
                first_name='Admin',
                last_name='Sistema',
                tipo='seguridad',
                rol='admin'
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe'))
