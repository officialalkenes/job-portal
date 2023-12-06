from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.db.models.functions import Now
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.profiles.models import UserProfile

from .models import UserActivity

User = get_user_model()


@receiver(user_logged_in)
def register_login(sender, user, request, **kwargs):
    UserActivity.objects.create(user=user, session_key=request.session.session_key)


@receiver(user_logged_out)
def register_logout(sender, user, request, **kwargs):
    UserActivity.objects.filter(
        user=user, session_key=request.session.session_key
    ).update(logout=Now())


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    return "user {} logged in through page {}".format(
        user.email, request.META.get("HTTP_REFERER")
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    return "user {} logged in failed through page {}".format(
        credentials.get("email"), request.META.get("HTTP_REFERER")
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    return "user {} logged out through page {}".format(
        user.email, request.META.get("HTTP_REFERER")
    )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, **kwargs):
    """
    A post-save signal handler for User instances.
    This function is triggered after a User instance is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
