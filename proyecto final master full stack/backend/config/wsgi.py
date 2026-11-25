"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# En Render el disco se borra al dormir. Cada arranque deja la demo lista.
if os.environ.get("RENDER"):
    from django.core.management import call_command

    call_command("migrate", interactive=False, verbosity=1)
    call_command("seed_demo")
    call_command("seed_admin")
