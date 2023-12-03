from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator

from djoser.serializers import UserCreateSerializer, UserSerializer
from djoser.serializers import TokenCreateSerializer
from rest_framework import serializers


User = get_user_model()


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
