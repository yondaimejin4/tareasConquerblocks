from django import forms
from django.contrib import admin
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.utils.html import format_html

from .models import ContactLead

User = get_user_model()


class UserContactLeadInline(admin.TabularInline):
    model = ContactLead
    fk_name = "user"
    extra = 0
    can_delete = False
    show_change_link = True
    verbose_name = "Solicitud (lead)"
    verbose_name_plural = "Solicitudes / leads del cliente"
    readonly_fields = (
        "id",
        "status",
        "payment_status",
        "company",
        "message_short",
        "updated_at",
    )
    fields = readonly_fields

    @admin.display(description="Mensaje")
    def message_short(self, obj):
        text = obj.message.strip()
        return text[:60] + "..." if len(text) > 60 else text


class ClientUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo")
    first_name = forms.CharField(required=False, label="Nombre")
    last_name = forms.CharField(required=False, label="Apellido")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class ClientUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_active")


class ClientUserAdmin(BaseUserAdmin):
    """Cuentas de clientes para el portal (/portal/login)."""

    add_form = ClientUserCreationForm
    form = ClientUserChangeForm

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "leads_count",
        "is_active",
        "date_joined",
    )
    inlines = [UserContactLeadInline]
    list_filter = ("is_active",)
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)
    filter_horizontal = ()

    fieldsets = (
        ("Cuenta portal", {"fields": ("username", "email", "first_name", "last_name")}),
        ("Estado", {"fields": ("is_active",)}),
    )
    readonly_fields = ("is_staff", "is_superuser")

    add_fieldsets = (
        (
            "Nuevo cliente",
            {
                "classes": ("wide",),
                "description": (
                    "El cliente iniciara sesion en /portal/login con el usuario y "
                    "contrasena que definas aqui. Sus solicitudes (leads) se gestionan "
                    "en la seccion inferior o en Solicitudes de clientes."
                ),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display(description="Solicitudes")
    def leads_count(self, obj):
        count = getattr(obj, "_leads_count", None)
        if count is None:
            count = obj.project_requests.count()
        if count == 0:
            return "0"
        url = (
            reverse("admin:core_contactlead_changelist")
            + f"?user__id__exact={obj.pk}"
        )
        return format_html('<a href="{}">{}</a>', url, count)

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(_leads_count=Count("project_requests"))
        if request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs.filter(is_staff=False, is_superuser=False)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("is_staff", "is_superuser")
        return ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_staff = False
            obj.is_superuser = False
        elif not obj.is_superuser:
            obj.is_staff = False
        super().save_model(request, obj, form, change)


if admin.site.is_registered(User):
    admin.site.unregister(User)
admin.site.register(User, ClientUserAdmin)
