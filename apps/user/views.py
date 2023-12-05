from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import permissions, status, response, views
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

from .serializers import SignUpUserSerializer

User = get_user_model()


class SignUpView(views.APIView):
    serializer_class = SignUpUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Send verification email
            self.send_verification_email(user.email, access_token)

            return response.Response(
                {"message": "User registered successfully. Verification email sent."},
                status=status.HTTP_201_CREATED,
            )

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_email(self, email, access_token):
        subject = "Verify Your Email"
        message = render_to_string(
            "verification_email_template.html",
            {"verification_url": self.get_verification_url(access_token)},
        )
        plain_message = strip_tags(message)
        from_email = "your_email@example.com"  # Update with your email
        recipient_list = [email]

        send_mail(
            subject, plain_message, from_email, recipient_list, html_message=message
        )

    def get_verification_url(self, access_token):
        # Replace 'your_frontend_url' with the actual URL where your frontend is hosted
        return f"localhost:8000/verify-email/?token={access_token}"
