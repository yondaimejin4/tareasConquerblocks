# ALPRO TECHNOLOGY SPA — Proyecto Final Máster Full Stack

Aplicación web full stack para una empresa de servicios tecnológicos: catálogo de servicios, formulario de contacto, portal del cliente y panel administrativo.

**Aplicación pública:** [https://alpro-pfm.onrender.com](https://alpro-pfm.onrender.com)

**Arranque local:** `./scripts/dev.sh` → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

| Superficie | URL | Acceso |
|------------|-----|--------|
| Sitio (React) | http://127.0.0.1:8000/ | Público |
| Portal cliente | http://127.0.0.1:8000/portal/login | Cuenta de cliente |
| Administración | http://127.0.0.1:8000/admin/ | `admin` / `Admin123` |

## Stack

| Capa | Tecnología |
|------|------------|
| Backend | Django 6, Django REST Framework, autenticación por sesión |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Frontend | React 19, Vite 8, React Router |
| Servidor | Django sirve la SPA compilada y la API en el mismo origen |
| Despliegue | [https://alpro-pfm.onrender.com](https://alpro-pfm.onrender.com) (Render, plan gratuito) |
| Pruebas | `python manage.py test core` |

## Qué resuelve

- El visitante consulta el catálogo real (`GET /api/services/`) y envía una consultoría (`POST /api/contact/`).
- El cliente entra al portal, crea solicitudes y ve el estado que marca el administrador.
- El administrador gestiona usuarios, el catálogo y el estado de cada solicitud desde Django Admin.
- Admin y portal usan cookies distintas (`sessionid` y `portal_sessionid`), así que ambas sesiones pueden convivir en el mismo navegador.

## Estructura

```
├── backend/          # Django: modelos, API, admin, plantillas, tests
├── frontend/         # React: landing y portal cliente
├── docs/             # Memoria técnica y guía de despliegue
├── scripts/          # dev.sh y verificar.sh
├── requirements.txt
├── build.sh
└── render.yaml
```

## Instalación

Requisitos: Python 3.13+ y Node.js 20+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

./scripts/dev.sh
```

El script aplica migraciones, carga el catálogo de demostración, crea el administrador, compila React y arranca el servidor en el puerto 8000.

### Desarrollo con recarga del frontend

Terminal 1: `cd backend && python manage.py runserver`  
Terminal 2: `cd frontend && npm install && npm run dev`

Vite hace proxy de `/api` y `/media` hacia el puerto 8000. Deja `VITE_API_BASE_URL` vacío.

## API

| Método | Ruta | Uso |
|--------|------|-----|
| GET | `/api/health/` | Estado del servicio |
| GET | `/api/services/` | Catálogo |
| GET | `/api/services/featured/` | Destacados |
| POST | `/api/contact/` | Consultoría pública |
| POST | `/api/auth/register/` `/login/` `/logout/` | Portal |
| GET | `/api/auth/me/` | Sesión del portal |
| GET/POST | `/api/my-requests/` | Solicitudes del cliente autenticado |
| GET | `/api/my-requests/<id>/` | Detalle de una solicitud propia |

## Roles

| Rol | Puede |
|-----|--------|
| Visitante | Ver servicios y enviar el formulario de consultoría |
| Cliente | Iniciar sesión, ver y crear sus propias solicitudes |
| Administrador | Django Admin: usuarios, catálogo y estado de cada solicitud |

En el admin, **Usuarios → Añadir usuario** crea la cuenta del portal. En cada solicitud se cambia el estado, y el cliente lo ve al recargar.

## Datos de demostración

```bash
cd backend
python manage.py seed_demo          # 16 servicios
python manage.py seed_demo --reset  # recarga el catálogo
python manage.py seed_admin         # admin / Admin123
```

## Tests

```bash
source .venv/bin/activate
cd backend
python manage.py test core
```

## Seguridad

- Contraseñas con el hasher de Django (PBKDF2).
- Validación en serializers de DRF.
- CSRF en el admin y en las peticiones del portal.
- El formulario público no reutiliza la sesión del administrador.
- Secretos y hosts por variables de entorno (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`).
- HTTPS en producción mediante el proveedor de despliegue.

## Documentación

- Memoria del PFM: [docs/Memoria_PFM_ALPRO.pdf](docs/Memoria_PFM_ALPRO.pdf)
- Despliegue gratis (PythonAnywhere): [docs/DEPLOY_PYTHONANYWHERE.md](docs/DEPLOY_PYTHONANYWHERE.md)
- Vídeo de defensa: [docs/video-defensa-pfm.mp4](docs/video-defensa-pfm.mp4)

Usuarios de prueba: administrador `admin` / `Admin123` · cliente `cliente_demo` / `Cliente123`

## Autor

Proyecto Final — Máster en Desarrollo Full Stack (ConquerBlocks)
