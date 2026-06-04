# Guia de despliegue — ALPRO PFM

## Opcion A: Render (recomendada)

1. Sube el repositorio a GitHub (publico).
2. En [Render](https://render.com), crea un **Blueprint** desde `render.yaml` o:
   - **Web Service** Python, build: `./build.sh`, start: `cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
   - **PostgreSQL** free y enlaza `DATABASE_URL`
3. Variables de entorno en el servicio web:
   - `DEBUG=False`
   - `SECRET_KEY` (generada)
   - `ALLOWED_HOSTS=tu-app.onrender.com`
   - `CORS_ALLOWED_ORIGINS=https://tu-frontend.onrender.com`
4. Frontend: **Static Site** con build `cd frontend && npm install && npm run build`, publish `frontend/dist`.
5. En el static site, variable `VITE_API_BASE_URL=https://tu-api.onrender.com` (configurar en build).

## Opcion B: Railway / VPS

Mismos pasos: instalar `requirements.txt`, `migrate`, `seed_demo`, `collectstatic`, gunicorn + nginx para static React.

## Post-despliegue

- Crear superusuario: `python manage.py createsuperuser`
- Ejecutar `seed_demo` si el catalogo esta vacio
- Actualizar README con URLs publicas antes de entregar el PFM
