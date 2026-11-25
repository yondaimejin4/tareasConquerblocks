from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Crea o actualiza el superusuario admin (usuario: admin, pass: Admin123)."

    def handle(self, *args, **options):
        username = "admin"
        password = "Admin123"
        email = "admin@alpro.local"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS("Superusuario admin creado."))
        else:
            self.stdout.write(self.style.SUCCESS("Superusuario admin actualizado."))

        client, client_created = User.objects.get_or_create(
            username="cliente_demo",
            defaults={
                "email": "cliente.demo@alpro.cl",
                "first_name": "Ana",
                "last_name": "Perez",
                "is_staff": False,
                "is_superuser": False,
            },
        )
        client.email = "cliente.demo@alpro.cl"
        client.first_name = "Ana"
        client.last_name = "Perez"
        client.is_staff = False
        client.is_superuser = False
        client.set_password("Cliente123")
        client.save()
        if client_created:
            self.stdout.write(self.style.SUCCESS("Cliente cliente_demo creado."))
        else:
            self.stdout.write(self.style.SUCCESS("Cliente cliente_demo actualizado."))
