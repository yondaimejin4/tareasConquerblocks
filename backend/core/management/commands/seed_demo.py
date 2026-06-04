from django.core.management.base import BaseCommand
from django.core.management import call_command

from core.models import Service


class Command(BaseCommand):
    help = "Carga servicios de demostracion si la base de datos esta vacia."

    def handle(self, *args, **options):
        if Service.objects.exists():
            self.stdout.write(self.style.WARNING("Ya existen servicios. No se cargaron datos."))
            return

        call_command("loaddata", "initial_data")
        self.stdout.write(self.style.SUCCESS("Servicios de demostracion cargados correctamente."))
