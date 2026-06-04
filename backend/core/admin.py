from django.contrib import admin

from .models import ContactLead, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "created_at")
    list_filter = ("is_featured",)
    search_fields = ("title", "short_description")
    ordering = ("-is_featured", "title")


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
