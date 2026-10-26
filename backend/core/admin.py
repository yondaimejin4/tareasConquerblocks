from django import forms
from django.contrib import admin
from django.utils.html import format_html

from . import admin_users  # noqa: F401 — registra User en el admin
from .models import ClientContribution, ContactLead, Service


class ContactLeadAdminForm(forms.ModelForm):
    class Meta:
        model = ContactLead
        fields = "__all__"
        widgets = {
            "team_comment": forms.Textarea(
                attrs={
                    "rows": 6,
                    "cols": 72,
                    "placeholder": (
                        "Ej.: Estamos revisando tu brief. Te enviaremos mockups la proxima semana."
                    ),
                }
            ),
            "pending_summary": forms.TextInput(
                attrs={
                    "size": 72,
                    "placeholder": "Ej.: Pendiente abono del 50% para iniciar desarrollo.",
                }
            ),
            "message": forms.Textarea(attrs={"rows": 4}),
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
        }


class ClientContributionInline(admin.TabularInline):
    model = ClientContribution
    extra = 0
    can_delete = False
    readonly_fields = ("user", "message", "attachment_link", "created_at")
    fields = ("user", "message", "attachment_link", "created_at")
    verbose_name = "Aporte del cliente"
    verbose_name_plural = "Aportes e ideas del cliente"

    @admin.display(description="Imagen")
    def attachment_link(self, obj):
        if obj.attachment:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">Ver imagen adjunta</a>',
                obj.attachment.url,
            )
        return "—"


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    form = ContactLeadAdminForm
    autocomplete_fields = ("user",)
    list_display = (
        "id",
        "name",
        "email",
        "user",
        "status",
        "payment_status",
        "has_team_comment",
        "contributions_count",
        "updated_at",
    )
    list_display_links = ("id", "name")
    list_editable = ("status", "payment_status")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = (
        "name",
        "email",
        "company",
        "message",
        "team_comment",
        "pending_summary",
        "user__username",
        "user__email",
    )
    readonly_fields = ("created_at", "updated_at", "contributions_count")
    date_hierarchy = "created_at"
    ordering = ("-updated_at",)
    inlines = [ClientContributionInline]
    save_on_top = True
    fieldsets = (
        (
            "Solicitud del cliente",
            {
                "fields": (
                    "user",
                    "name",
                    "email",
                    "company",
                    "message",
                    "contributions_count",
                ),
                "description": (
                    "Mensaje inicial y aportes del cliente (mas abajo). "
                    "Guarda los cambios de estado al final de la pagina."
                ),
            },
        ),
        (
            "Estado del proyecto (visible en portal)",
            {
                "fields": ("status", "team_comment"),
                "description": (
                    "Elige el estado y escribe un comentario: el cliente lo vera en "
                    "/portal/solicitudes al abrir el detalle."
                ),
            },
        ),
        (
            "Estado de pago (visible en portal)",
            {
                "fields": ("payment_status", "pending_summary"),
                "description": (
                    "Modifica el estado de pago y, si aplica, el detalle. "
                    "El cliente ve ambos en su panel."
                ),
            },
        ),
        (
            "Notas internas",
            {
                "fields": ("admin_notes",),
                "classes": ("collapse",),
                "description": "No se muestran al cliente.",
            },
        ),
        ("Fechas", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Aportes")
    def contributions_count(self, obj):
        return obj.contributions.count()

    @admin.display(boolean=True, description="Comentario")
    def has_team_comment(self, obj):
        return bool(obj.team_comment.strip())


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("title", "short_description")


@admin.register(ClientContribution)
class ClientContributionAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "user", "message_preview", "has_attachment", "created_at")
    list_filter = ("created_at",)
    search_fields = ("message", "lead__name", "lead__email", "user__username")
    readonly_fields = ("lead", "user", "message", "attachment_link", "created_at")
    date_hierarchy = "created_at"

    @admin.display(description="Mensaje")
    def message_preview(self, obj):
        text = obj.message.strip()
        return text[:80] + "..." if len(text) > 80 else text

    @admin.display(boolean=True, description="Imagen")
    def has_attachment(self, obj):
        return bool(obj.attachment)

    @admin.display(description="Adjunto")
    def attachment_link(self, obj):
        if obj.attachment:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener">Ver imagen</a>',
                obj.attachment.url,
            )
        return "—"
