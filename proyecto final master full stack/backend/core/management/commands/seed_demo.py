from django.core.management.base import BaseCommand
from django.core.management import call_command

from core.models import Service


class Command(BaseCommand):
    help = "Carga servicios de demostracion. Usa --reset para recargar el catalogo completo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Elimina servicios existentes y vuelve a cargar los fixtures.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted, _ = Service.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Eliminados {deleted} servicios."))

        if Service.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Ya existen servicios. Usa --reset para recargar el catalogo ampliado."
                )
            )
            return

        call_command("loaddata", "initial_data")
        count = Service.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Catalogo cargado: {count} servicios de demostracion.")
        )
