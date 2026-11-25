# Despliegue gratis en PythonAnywhere

URL final: `https://TU_USUARIO.pythonanywhere.com`

No hace falta tarjeta. El plan Beginner es gratuito. La app gratis caduca al mes si no la usas: publícala cerca de la defensa.

## 0. Antes de empezar

1. Crea la cuenta Beginner (gratis):  
   https://www.pythonanywhere.com/registration/register/beginner/
2. Anota tu usuario. La web quedará en `https://TU_USUARIO.pythonanywhere.com`.
3. En este Mac ya debe estar el frontend compilado (`frontend/dist`) y subido a GitHub.

## 1. Clonar el repo (consola Bash)

```bash
cd ~
git clone https://github.com/yondaimejin4/tareasConquerblocks.git
cd "tareasConquerblocks/proyecto final master full stack"
```

## 2. Entorno virtual e instalación

Usa Python **3.12** o **3.13** (Django 6 lo exige):

```bash
mkvirtualenv --python=/usr/bin/python3.12 alpro-pfm
pip install -r requirements.txt
```

Si `python3.12` no existe, prueba `python3.13`. Si ninguno está, elige la versión más alta disponible en el menú de la web app y avisa.

## 3. Base de datos y estáticos

```bash
cd ~/tareasConquerblocks/proyecto\ final\ master\ full\ stack/backend
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_demo
python manage.py seed_admin
```

Credenciales de demo:

- Admin: `admin` / `Admin123`
- Cliente: `cliente_demo` / `Cliente123`

## 4. Crear la web app

1. Ve a **Web** → **Add a new web app**.
2. Elige **Manual configuration** (no el wizard de Django).
3. Python 3.12 (o 3.13).
4. En **Virtualenv**: `/home/TU_USUARIO/.virtualenvs/alpro-pfm`
5. Abre el archivo **WSGI configuration file** y déjalo así (cambia `TU_USUARIO`):

```python
import os
import sys

project = "/home/TU_USUARIO/tareasConquerblocks/proyecto final master full stack"
backend = project + "/backend"

if backend not in sys.path:
    sys.path.insert(0, backend)

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
os.environ["DEBUG"] = "False"
os.environ["SECRET_KEY"] = "cambia-esta-clave-larga-y-aleatoria"
os.environ["ALLOWED_HOSTS"] = "TU_USUARIO.pythonanywhere.com"
os.environ["CORS_ALLOWED_ORIGINS"] = "https://TU_USUARIO.pythonanywhere.com"
os.environ["SECURE_SSL_REDIRECT"] = "False"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. **Static files** (opcional si WhiteNoise ya sirve todo; útil para el admin):

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/TU_USUARIO/tareasConquerblocks/proyecto final master full stack/backend/staticfiles/` |
| `/media/` | `/home/TU_USUARIO/tareasConquerblocks/proyecto final master full stack/backend/media/` |

7. Pulsa **Reload**.

## 5. Comprobar

- Landing: `https://TU_USUARIO.pythonanywhere.com/`
- API: `https://TU_USUARIO.pythonanywhere.com/api/services/`
- Admin: `https://TU_USUARIO.pythonanywhere.com/admin/`
- Portal: `https://TU_USUARIO.pythonanywhere.com/portal/login`

## Actualizar después de un push

```bash
cd ~/tareasConquerblocks
git pull
workon alpro-pfm
cd "proyecto final master full stack/backend"
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

Luego **Reload** en la pestaña Web.

## Si el disco se llena (512 MiB)

No instales `frontend/node_modules` en PythonAnywhere. El React ya viene compilado en `frontend/dist` desde este repositorio.
