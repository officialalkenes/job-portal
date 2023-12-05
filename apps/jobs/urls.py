from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.AllJobs.as_view(), name="all-jobs"),
    path("create-job", views.CreateJob.as_view(), name="create-job"),
    path("job/<str:uuid>/", views.GetUpdateJob.as_view(), name="get-job"),
]
