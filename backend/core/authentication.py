from rest_framework.authentication import BaseAuthentication

from .portal_auth import get_portal_user


class PortalSessionAuthentication(BaseAuthentication):
    """Solo la cookie portal_sessionid; ignora la sesion del admin Django."""

    def authenticate(self, request):
        user = get_portal_user(request)
        if user is None:
            return None
        return (user, None)
