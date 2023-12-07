from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.AllJobs.as_view(), name="all-jobs"),
    path("create-job", views.CreateJob.as_view(), name="create-job"),
    path("job/<str:uuid>/", views.GetUpdateJob.as_view(), name="get-job"),
    path("stats/<str:topic>/", views.GetJobStatView.as_view(), name="get-job-stat"),
    path("jobs/<int:job_id>/apply/", views.ApplyJobView.as_view(), name="apply_job"),
    path("my-applied-jobs/", views.MyJobAppliedViews.as_view(), name="my_applied_jobs"),
    path(
        "jobs/<int:job_id>/candidates/",
        views.ListCandidatesView.as_view(),
        name="list_candidates",
    ),
]
