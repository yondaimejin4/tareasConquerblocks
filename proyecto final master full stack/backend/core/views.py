from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import PortalSessionAuthentication
from .models import ClientContribution, ContactLead, Service
from .portal_auth import (
    attach_portal_cookie,
    clear_portal_cookie,
    get_portal_user,
    portal_login,
    portal_logout,
)
from .serializers import (
    ClientContributionSerializer,
    ContactLeadCreateSerializer,
    ContributionCreateSerializer,
    LoginSerializer,
    ProjectRequestCreateSerializer,
    ProjectRequestListSerializer,
    ProjectRequestSerializer,
    RegisterSerializer,
    ServiceSerializer,
    UserSerializer,
)


class HealthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from .spa_views import react_dist_ready

        total = Service.objects.count()
        featured = Service.objects.filter(is_featured=True).count()
        return Response(
            {
                "ok": True,
                "services_total": total,
                "services_featured": featured,
                "react_build": react_dist_ready(),
            }
        )


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_services"] = Service.objects.filter(is_featured=True)[:3]
        context["all_services_count"] = Service.objects.count()
        context["leads_count"] = ContactLead.objects.count()
        return context


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all().order_by("-is_featured", "title")
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


class FeaturedServiceListAPIView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Service.objects.filter(is_featured=True).order_by("title")


class ContactLeadCreateAPIView(APIView):
    """Formulario publico: sin sesion Django admin (evita CSRF por cookie de /admin/)."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ContactLeadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        portal_user = get_portal_user(request)
        ContactLead.objects.create(
            user=portal_user,
            **data,
        )
        return Response(
            {"message": "Gracias. Hemos recibido tu solicitud y te contactaremos pronto."},
            status=status.HTTP_201_CREATED,
        )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfCookieAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        session_key = portal_login(user)
        response = Response(
            {"user": UserSerializer(user).data, "message": "Cuenta creada correctamente."},
            status=status.HTTP_201_CREATED,
        )
        return attach_portal_cookie(response, session_key)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Usuario o contrasena incorrectos."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        session_key = portal_login(user)
        response = Response({"user": UserSerializer(user).data})
        return attach_portal_cookie(response, session_key)


class LogoutAPIView(APIView):
    authentication_classes = [PortalSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        portal_logout(request)
        response = Response({"message": "Sesion cerrada."})
        return clear_portal_cookie(response)


class MeAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        user = get_portal_user(request)
        if user is None:
            return Response({"authenticated": False})
        return Response(
            {
                "authenticated": True,
                "user": UserSerializer(user).data,
                "is_staff": user.is_staff,
            }
        )


class MyProjectRequestListCreateAPIView(APIView):
    authentication_classes = [PortalSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ContactLead.objects.filter(user=request.user).prefetch_related(
            "contributions"
        )
        serializer = ProjectRequestListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectRequestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        name = request.user.get_full_name().strip() or request.user.username
        lead = ContactLead.objects.create(
            user=request.user,
            name=name,
            email=request.user.email,
            company=data.get("company", ""),
            message=data["message"],
        )
        return Response(
            ProjectRequestSerializer(lead, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class MyProjectRequestDetailAPIView(APIView):
    authentication_classes = [PortalSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return ContactLead.objects.prefetch_related("contributions").get(
            pk=pk, user=request.user
        )

    def get(self, request, pk):
        try:
            lead = self.get_object(request, pk)
        except ContactLead.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectRequestSerializer(lead, context={"request": request})
        return Response(serializer.data)


class MyContributionCreateAPIView(APIView):
    authentication_classes = [PortalSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            lead = ContactLead.objects.get(pk=pk, user=request.user)
        except ContactLead.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContributionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contribution = ClientContribution.objects.create(
            lead=lead,
            user=request.user,
            message=serializer.validated_data["message"],
            attachment=serializer.validated_data.get("attachment"),
        )
        return Response(
            ClientContributionSerializer(contribution, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
