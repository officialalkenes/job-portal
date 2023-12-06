from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

from djoser.serializers import UserCreateSerializer, UserSerializer
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers


User = get_user_model()


class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False, "min_length": 8},
        }


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )

    email = serializers.EmailField(
        validators=[EmailValidator()],
        required=True,
    )
