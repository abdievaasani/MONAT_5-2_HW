from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from users.models import CustomUser


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("User already exists")
        return email

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", "")
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["email"],   # тут исправлено
            password=attrs["password"]
        )

        if not user:
            raise ValidationError("Invalid email or password")

        attrs["user"] = user
        return attrs


class ConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)