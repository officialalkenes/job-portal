from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.AllJobs.as_view(), name="all-jobs"),
]
