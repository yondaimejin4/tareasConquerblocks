"""Sesion del portal cliente, separada de la sesion del admin Django."""

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

PORTAL_SESSION_COOKIE_NAME = "portal_sessionid"


def _portal_store(session_key=None):
    return SessionStore(session_key=session_key)


def portal_login(user):
    store = _portal_store()
    store[SESSION_KEY] = str(user.pk)
    store[BACKEND_SESSION_KEY] = "django.contrib.auth.backends.ModelBackend"
    store.save()
    return store.session_key


def portal_logout(request):
    session_key = request.COOKIES.get(PORTAL_SESSION_COOKIE_NAME)
    if not session_key:
        return
    store = _portal_store(session_key)
    if store.exists(session_key):
        store.flush()


def get_portal_user(request):
    session_key = request.COOKIES.get(PORTAL_SESSION_COOKIE_NAME)
    if not session_key:
        return None
    store = _portal_store(session_key)
    if not store.exists(session_key):
        return None
    user_id = store.get(SESSION_KEY)
    if not user_id:
        return None
    User = get_user_model()
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


def _cookie_kwargs():
    secure = getattr(settings, "SESSION_COOKIE_SECURE", False)
    if settings.DEBUG:
        secure = False
    return {
        "max_age": settings.SESSION_COOKIE_AGE,
        "httponly": settings.SESSION_COOKIE_HTTPONLY,
        "samesite": settings.SESSION_COOKIE_SAMESITE,
        "secure": secure,
        "path": "/",
    }


def attach_portal_cookie(response, session_key):
    response.set_cookie(PORTAL_SESSION_COOKIE_NAME, session_key, **_cookie_kwargs())
    return response


def clear_portal_cookie(response):
    response.delete_cookie(
        PORTAL_SESSION_COOKIE_NAME,
        path="/",
        samesite=settings.SESSION_COOKIE_SAMESITE,
    )
    return response
