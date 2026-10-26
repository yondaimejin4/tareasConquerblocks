from django.conf import settings
from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=200)
    details = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContactLead(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Recibida"
        REVIEW = "review", "En revision"
        IN_PROGRESS = "in_progress", "En desarrollo"
        DONE = "done", "Entregada"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pendiente"
        PARTIAL = "partial", "Pago parcial"
        PAID = "paid", "Pagado"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="project_requests",
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
        verbose_name="Estado del proyecto",
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name="Estado de pago",
    )
    pending_summary = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Detalle de pago para el cliente",
        help_text="Ej.: Falta transferencia del 50%. El cliente lo ve en su portal.",
    )
    team_comment = models.TextField(
        blank=True,
        verbose_name="Comentario del estado del proyecto",
        help_text="Explica en que fase va el proyecto. Se actualiza en el portal del cliente.",
    )
    admin_notes = models.TextField(
        blank=True,
        help_text="Notas internas solo para el equipo ALPRO (no visibles al cliente).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        verbose_name = "Solicitud de cliente"
        verbose_name_plural = "Solicitudes de clientes"

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class ClientContribution(models.Model):
    lead = models.ForeignKey(
        ContactLead,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    message = models.TextField()
    attachment = models.ImageField(
        upload_to="contributions/%Y/%m/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Aporte #{self.pk} - solicitud {self.lead_id}"
