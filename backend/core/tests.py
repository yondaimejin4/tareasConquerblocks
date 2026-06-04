from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactLead, Service


class ServiceAPITests(APITestCase):
    def setUp(self):
        Service.objects.create(
            title="Servicio test",
            short_description="Descripcion corta",
            details="Detalle completo del servicio.",
            is_featured=True,
        )

    def test_list_services_returns_json(self):
        url = reverse("service-list-api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Servicio test")

    def test_featured_services_only_returns_featured(self):
        Service.objects.create(
            title="No destacado",
            short_description="x",
            details="y",
            is_featured=False,
        )
        url = reverse("service-featured-api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]["is_featured"])


class ContactAPITests(APITestCase):
    def test_create_contact_lead_success(self):
        url = reverse("contact-create-api")
        payload = {
            "name": "Maria Lopez",
            "email": "maria@empresa.com",
            "company": "Empresa Demo",
            "message": "Necesitamos una web corporativa.",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactLead.objects.count(), 1)
        self.assertIn("Gracias", response.data["message"])

    def test_create_contact_lead_invalid_email(self):
        url = reverse("contact-create-api")
        payload = {
            "name": "Juan",
            "email": "correo-invalido",
            "message": "Hola",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactLead.objects.count(), 0)
