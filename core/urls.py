from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from rest_framework_simplejwt.views import TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Jobify API",
        default_version="v1",
        description="Linkedin-like Api for app",
        terms_of_service="https://newcodecrafters.com/api/terms/",
        contact=openapi.Contact(email="developer@newcodecrafters.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("secret/", admin.site.urls),
    path("auth/", include("djoser.social.urls")),
    path("api-auth/", include("rest_framework.urls")),
    # Include Djoser URL patterns
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),  # Optional: Include JWT token endpoints
    path(
        "auth/", include("apps.user.urls", namespace="user")
    ),  # Optional: Include JWT token endpoints
    path("jobs/", include("apps.jobs.urls", namespace="jobs")),
    # path("skills/", include("apps.skills.urls", namespace="skills")),
]

# Custom Exception
handler500 = "apps.jobs.utils.handler500"
handler404 = "apps.jobs.utils.handler404"

# Rest Framework
# handler400 = 'rest_framework.exceptions.bad_request'
# handler500 = 'rest_framework.exceptions.server_error'
