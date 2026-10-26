from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactLead, Service
from .portal_auth import PORTAL_SESSION_COOKIE_NAME, portal_login

User = get_user_model()


def portal_force_login(client, user):
    client.cookies[PORTAL_SESSION_COOKIE_NAME] = portal_login(user)


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

    def test_create_contact_with_admin_session_cookie_succeeds(self):
        """Con sesion de /admin/ abierta el formulario publico debe seguir funcionando."""
        admin = User.objects.create_superuser(
            username="admin_contact",
            email="admin_contact@test.com",
            password="AdminContact123!",
        )
        self.client.force_login(admin)
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
        lead = ContactLead.objects.first()
        self.assertIsNone(lead.user)

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


class PortalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cliente1",
            email="cliente1@test.com",
            password="Password123!",
        )

    def test_register_and_list_own_requests(self):
        register_url = reverse("auth-register")
        response = self.client.post(
            register_url,
            {
                "username": "nuevo",
                "email": "nuevo@test.com",
                "password": "Password123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        list_url = reverse("my-requests-list")
        create_response = self.client.post(
            list_url,
            {"company": "ACME", "message": "Quiero una tienda online"},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["status"], "received")

    def test_client_cannot_see_other_users_request(self):
        portal_force_login(self.client, self.user)
        mine = ContactLead.objects.create(
            user=self.user,
            name="Cliente",
            email="cliente1@test.com",
            message="Mi proyecto",
        )
        other = User.objects.create_user(
            username="otro",
            email="otro@test.com",
            password="Password123!",
        )
        ContactLead.objects.create(
            user=other,
            name="Otro",
            email="otro@test.com",
            message="Otro proyecto",
        )

        url = reverse("my-requests-detail", kwargs={"pk": mine.pk})
        ok = self.client.get(url)
        self.assertEqual(ok.status_code, status.HTTP_200_OK)

        url_other = reverse("my-requests-detail", kwargs={"pk": other.pk})
        forbidden = self.client.get(url_other)
        self.assertEqual(forbidden.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_django_session_does_not_bleed_into_portal(self):
        """Sesion del panel /admin/ no debe usarse en el portal cliente."""
        admin = User.objects.create_superuser(
            username="admin_sep",
            email="admin_sep@test.com",
            password="AdminSep123!",
        )
        client_user = User.objects.create_user(
            username="cliente_sep",
            email="cliente_sep@test.com",
            password="ClienteSep123!",
        )
        self.client.force_login(admin)

        me = self.client.get(reverse("auth-me"))
        self.assertEqual(me.status_code, 200)
        self.assertFalse(me.data.get("authenticated"))

        login = self.client.post(
            reverse("auth-login"),
            {"username": "cliente_sep", "password": "ClienteSep123!"},
            format="json",
        )
        self.assertEqual(login.status_code, 200)

        create = self.client.post(
            reverse("my-requests-list"),
            {"company": "ACME", "message": "Solicitud como cliente"},
            format="json",
        )
        self.assertEqual(create.status_code, 201)
        lead = ContactLead.objects.get(pk=create.data["id"])
        self.assertEqual(lead.user_id, client_user.id)
        self.assertNotEqual(lead.user_id, admin.id)

    def test_client_sees_admin_team_comment_and_contributions(self):
        portal_force_login(self.client, self.user)
        create = self.client.post(
            reverse("my-requests-list"),
            {"company": "TestCo", "message": "Proyecto web"},
            format="json",
        )
        lead_id = create.data["id"]
        self.client.post(
            reverse("my-requests-contribution", kwargs={"pk": lead_id}),
            {"message": "Idea: usar colores corporativos"},
            format="json",
        )
        lead = ContactLead.objects.get(pk=lead_id)
        lead.status = ContactLead.Status.IN_PROGRESS
        lead.payment_status = ContactLead.PaymentStatus.PARTIAL
        lead.pending_summary = "Falta abono del 50%"
        lead.team_comment = "Estamos disenando el mockup inicial."
        lead.save()

        detail = self.client.get(reverse("my-requests-detail", kwargs={"pk": lead_id}))
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["team_comment"], lead.team_comment)
        self.assertEqual(detail.data["payment_status"], "partial")
        self.assertEqual(len(detail.data["contributions"]), 1)
        self.assertIn("colores corporativos", detail.data["contributions"][0]["message"])

    def test_admin_created_client_can_login(self):
        """Cuenta creada como en el admin (usuario + contrasena) puede entrar al portal."""
        User.objects.create_user(
            username="cliente_admin",
            email="cliente@empresa.com",
            password="ClaveAdmin123!",
            first_name="Ana",
            last_name="Perez",
            is_staff=False,
            is_superuser=False,
        )
        login_url = reverse("auth-login")
        response = self.client.post(
            login_url,
            {"username": "cliente_admin", "password": "ClaveAdmin123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "cliente_admin")
        self.assertEqual(response.data["user"]["email"], "cliente@empresa.com")
