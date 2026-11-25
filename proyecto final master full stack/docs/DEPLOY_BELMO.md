# Despliegue gratis en Belmo

URL final: `https://algo.app.belmo.io` (Belmo la asigna al crear el servicio).

Plan Starter: $0, sin tarjeta, la app no se duerme.

## 1. Crear cuenta

1. Entra en https://belmo.io
2. Regístrate / inicia sesión **con GitHub** (yondaimejin4).
3. Instala la **Belmo GitHub App** y dale acceso al repo  
   `yondaimejin4/tareasConquerblocks`.

## 2. Crear el servicio

1. Dashboard → **New service** → **API** (o Web).
2. Repo: `tareasConquerblocks`
3. Branch: `main`
4. **Root directory** (importante):  
   `proyecto final master full stack`
5. Si pide comandos a mano:

**Build:**

```bash
pip install -r requirements.txt && cd backend && python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py seed_demo && python manage.py seed_admin
```

**Start:**

```bash
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

## 3. Variables de entorno

En el panel del servicio:

| Variable | Valor |
|----------|--------|
| `DEBUG` | `False` |
| `SECRET_KEY` | una cadena larga aleatoria (Belmo puede generarla) |
| `ALLOWED_HOSTS` | `.app.belmo.io,.belmo.io,localhost` |
| `CORS_ALLOWED_ORIGINS` | `https://TU-SERVICIO.app.belmo.io` (la URL exacta que te den) |
| `SECURE_SSL_REDIRECT` | `False` |

Si Belmo te da `DATABASE_URL` (Postgres), déjala. Si no, el proyecto usa SQLite solo.

Tras el primer deploy, actualiza `CORS_ALLOWED_ORIGINS` y `ALLOWED_HOSTS` con el host real y vuelve a desplegar o reinicia.

## 4. Comprobar

- Landing: `https://TU-SERVICIO.app.belmo.io/`
- API: `/api/services/`
- Admin: `/admin/` → `admin` / `Admin123`
- Portal: `/portal/login` → `cliente_demo` / `Cliente123`

## Si falla la detección de Django

Belmo busca `manage.py`. En este repo está en `backend/`. Con el root directory apuntando a `proyecto final master full stack` y los comandos de arriba, no hace falta que lo detecte solo.
