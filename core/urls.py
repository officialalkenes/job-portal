from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
]

if settings.DEBUG:
    # Not for production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    