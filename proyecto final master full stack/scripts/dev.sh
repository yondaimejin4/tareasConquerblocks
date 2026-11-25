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
echo "== Compilando frontend (se actualiza solo al guardar) =="
cd "$ROOT/frontend"
npm run watch &
WATCH_PID=$!
cleanup() {
  kill "$WATCH_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
for _ in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30; do
  if [ -f dist/index.html ]; then
    break
  fi
  sleep 1
done

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
