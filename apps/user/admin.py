from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from django.utils.translation import gettext_lazy as _


from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("AUTHENTICATION_FIELD"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display_links = ["email"]
    list_display = ["email", "phone_number", "first_name", "last_name"]
    list_filter = (
        "is_superuser",
        "is_active",
    )
    search_fields = ("email", "phone_number")
    ordering = ("email",)
    filter_horizontal = ("user_permissions",)
