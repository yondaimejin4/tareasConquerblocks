from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "short_description",
            "details",
            "is_featured",
        ]


class ContactLeadCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    company = serializers.CharField(max_length=120, required=False, allow_blank=True)
    message = serializers.CharField()
