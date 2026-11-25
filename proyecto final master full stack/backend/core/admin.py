from django import forms
from django.contrib import admin

from . import admin_users  # noqa: F401 — registra User en el admin
from .models import ContactLead, Service


class ContactLeadAdminForm(forms.ModelForm):
    class Meta:
        model = ContactLead
        fields = "__all__"
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
            "admin_notes": forms.Textarea(attrs={"rows": 3}),
        }


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
        "updated_at",
    )
    list_display_links = ("id", "name")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = (
        "name",
        "email",
        "company",
        "message",
        "user__username",
        "user__email",
    )
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-updated_at",)
    save_on_top = True
    fieldsets = (
        (
            "Solicitud del cliente",
            {
                "fields": ("user", "name", "email", "company", "message"),
            },
        ),
        (
            "Estado (visible en el portal)",
            {"fields": ("status",)},
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("title", "short_description")

