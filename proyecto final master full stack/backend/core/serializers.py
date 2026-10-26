from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import ClientContribution, ContactLead, Service

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este usuario ya existe.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo ya esta registrado.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ClientContributionSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientContribution
        fields = ["id", "message", "attachment_url", "created_at"]

    def get_attachment_url(self, obj):
        if obj.attachment:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.attachment.url)
            return obj.attachment.url
        return None


class ProjectRequestSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_label = serializers.CharField(
        source="get_payment_status_display",
        read_only=True,
    )
    contributions = ClientContributionSerializer(many=True, read_only=True)

    class Meta:
        model = ContactLead
        fields = [
            "id",
            "name",
            "email",
            "company",
            "message",
            "status",
            "status_label",
            "payment_status",
            "payment_status_label",
            "pending_summary",
            "team_comment",
            "created_at",
            "updated_at",
            "contributions",
        ]


class ProjectRequestListSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    payment_status_label = serializers.CharField(
        source="get_payment_status_display",
        read_only=True,
    )

    class Meta:
        model = ContactLead
        fields = [
            "id",
            "name",
            "company",
            "message",
            "status",
            "status_label",
            "payment_status",
            "payment_status_label",
            "pending_summary",
            "team_comment",
            "created_at",
            "updated_at",
        ]


class ProjectRequestCreateSerializer(serializers.Serializer):
    company = serializers.CharField(max_length=120, required=False, allow_blank=True)
    message = serializers.CharField()


class ContributionCreateSerializer(serializers.Serializer):
    message = serializers.CharField()
    attachment = serializers.ImageField(required=False, allow_null=True)
