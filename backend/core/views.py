from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContactLead, Service
from .serializers import ContactLeadCreateSerializer, ServiceSerializer


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


class FeaturedServiceListAPIView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(is_featured=True).order_by("title")


class ContactLeadCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactLeadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ContactLead.objects.create(**serializer.validated_data)
        return Response(
            {"message": "Gracias. Hemos recibido tu solicitud y te contactaremos pronto."},
            status=status.HTTP_201_CREATED,
        )
