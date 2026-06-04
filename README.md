# ALPRO TECHNOLOGY SPA — Proyecto Final Master Full Stack

Aplicacion web full stack para una empresa de servicios tecnologicos: catalogo de servicios, captacion de leads y panel administrativo.

## Stack

| Capa | Tecnologia |
|------|------------|
| Backend | Django 6, Django REST Framework, SQLite (dev) / PostgreSQL (prod) |
| Frontend | React 19, Vite 8 |
| API | REST: `/api/services/`, `/api/services/featured/`, `/api/contact/` |
| Despliegue | Render (ver `render.yaml` y `docs/DEPLOY.md`) |

## Estructura

```
├── backend/          # Proyecto Django (models, API, templates, admin)
├── frontend/         # SPA React
├── docs/             # Memoria PFM y guia de despliegue
├── requirements.txt
├── build.sh          # Build para Render
└── render.yaml       # Blueprint de despliegue
```

## Requisitos

- Python 3.13+
- Node.js 20+

## Instalacion local

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # opcional, ajustar variables

cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

API y admin: `http://127.0.0.1:8000` · Admin: `http://127.0.0.1:8000/admin/`

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

App React: `http://127.0.0.1:5173`

Variable `VITE_API_BASE_URL` debe apuntar al backend (por defecto `http://127.0.0.1:8000`).

## Datos de demostracion

```bash
cd backend
python manage.py seed_demo
```

Carga 6 servicios (3 destacados) desde `core/fixtures/initial_data.json`.

## Tests

```bash
source .venv/bin/activate
cd backend
python manage.py test core
```

## Integracion React + Django (PFM)

- `GET /api/services/` — catalogo completo en React
- `GET /api/services/featured/` — servicios destacados
- `POST /api/contact/` — formulario de contacto persistido en `ContactLead`

## Seguridad

- Autenticacion Django para admin y `/accounts/login/`
- Validacion DRF en API de contacto
- CSRF en formularios de plantillas Django
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` y `CORS_ALLOWED_ORIGINS` por variables de entorno
- HTTPS recomendado en produccion (Render lo provee)

## Despliegue

Instrucciones detalladas en [docs/DEPLOY.md](docs/DEPLOY.md).

## Documentacion academica

Memoria tecnica (borrador para PDF): [docs/pfm-memoria.md](docs/pfm-memoria.md)

## Autor

Proyecto Final — Master en Desarrollo Full Stack (ConquerBlocks)
