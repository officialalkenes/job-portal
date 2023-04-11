import datetime

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.db import models
from django.db.models.functions import Now
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email Address"),
        help_text=_("Provide a Valid Email Address"),
    )
    admission_number = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(
        max_length=11, verbose_name=_("User's Phone Number"), blank=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can has teacher's/staff's Priviledges."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last Login Date"), auto_now=True)

    is_verified = models.BooleanField(
        _("email_verify"),
        default=False,
        help_text=_("Designates whether this user's email has been Verified. "),
    )

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_local_today(self) -> datetime.date:
        """
        Auto Detect Current User's timezone.
        localdate
        """
        return timezone.localdate()

    # @property
    # def get_shortname(self):
    #     return f"{self.first_name}"

    def __str__(self) -> str:
        return f"{self.email}"

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, db_index=True, null=True, blank=True)
    login = models.DateTimeField(auto_now_add=True)
    logout = models.DateTimeField(null=True, default=None)


class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user: {}, attempts: {}".format(self.user.email, self.login_attempts)


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
