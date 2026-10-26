#!/usr/bin/env bash
# Modo recomendado: un solo puerto (8000). Backend + React compilado.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

source .venv/bin/activate

echo "== Preparando backend =="
cd backend
python manage.py migrate --noinput
python manage.py seed_demo 2>/dev/null || true
python manage.py seed_admin

echo ""
echo "== Compilando frontend =="
cd "$ROOT/frontend"
npm run build

echo ""
echo "== Iniciando servidor =="
cd "$ROOT/backend"
echo ""
echo "  Web (React):  http://127.0.0.1:8000/"
echo "  Portal:       http://127.0.0.1:8000/portal/login"
echo "  Admin:        http://127.0.0.1:8000/admin/  (admin / Admin123)"
echo "  Django HTML:  http://127.0.0.1:8000/django/"
echo ""
python manage.py runserver
