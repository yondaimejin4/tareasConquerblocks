from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.views import View

FRONTEND_DIST = Path(settings.BASE_DIR).parent / "frontend" / "dist"


def _dist_file(path_parts):
    try:
        file_path = FRONTEND_DIST.joinpath(*path_parts).resolve()
        file_path.relative_to(FRONTEND_DIST.resolve())
    except (ValueError, OSError):
        return None
    if file_path.is_file():
        return file_path
    return None


class ReactAssetView(View):
    def get(self, request, filepath):
        file_path = _dist_file(["assets", filepath])
        if not file_path:
            return HttpResponse(status=404)
        return FileResponse(open(file_path, "rb"))


class ReactFaviconView(View):
    def get(self, request):
        file_path = _dist_file(["favicon.svg"])
        if not file_path:
            return HttpResponse(status=404)
        return FileResponse(open(file_path, "rb"), content_type="image/svg+xml")


class ReactSpaView(View):
    def get(self, request):
        file_path = _dist_file(["index.html"])
        if not file_path:
            return HttpResponse(
                "<h1>Frontend no compilado</h1>"
                "<p>Ejecuta: <code>cd frontend && npm run build</code></p>"
                "<p>O usa modo desarrollo: <code>cd frontend && npm run dev</code></p>",
                status=503,
                content_type="text/html; charset=utf-8",
            )
        return FileResponse(
            open(file_path, "rb"),
            content_type="text/html; charset=utf-8",
        )


def react_dist_ready():
    return (FRONTEND_DIST / "index.html").is_file()
