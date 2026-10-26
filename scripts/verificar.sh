#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
source .venv/bin/activate

echo "== Servicios en base de datos =="
cd backend
python manage.py shell -c "from core.models import Service; print('Total:', Service.objects.count()); print('Destacados:', Service.objects.filter(is_featured=True).count())"

echo ""
echo "== Admin =="
python manage.py seed_admin 2>&1 | tail -3

echo ""
echo "== Build React =="
cd "$ROOT/frontend"
npm run build -s

echo ""
echo "== API Django =="
if curl -sf http://127.0.0.1:8000/api/services/ >/dev/null; then
  COUNT=$(curl -s http://127.0.0.1:8000/api/services/ | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
  echo "OK - $COUNT servicios en /api/services/"
else
  echo "FALLO - Ejecuta: ./scripts/dev.sh"
  exit 1
fi

echo ""
echo "== Web React en :8000 =="
if curl -sf http://127.0.0.1:8000/ | grep -q "id=\"root\""; then
  echo "OK - Abre http://127.0.0.1:8000/"
else
  echo "FALLO - Frontend no servido. Ejecuta: cd frontend && npm run build"
  exit 1
fi

echo ""
echo "Todo correcto. Usa SOLO: http://127.0.0.1:8000/"
