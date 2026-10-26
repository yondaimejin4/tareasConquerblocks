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

        self.stdout.write(f"Usuario: {username}")
        self.stdout.write(f"Contrasena: {password}")
        self.stdout.write("Panel: http://127.0.0.1:8000/admin/")
