from django.db import models
from django.contrib.auth import get_user_model
from apps.jobs.models import JobListing  # Assuming you have a JobListing model

User = get_user_model()


class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_name = models.CharField(max_length=255)
    location = models.CharField(
        max_length=255
    )  # You might have additional fields for filtering
    job_type = models.CharField(max_length=20)
    industry = models.CharField(max_length=20)
    # Add more fields as needed


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
