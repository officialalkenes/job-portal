from django.db import models

from django.contrib.auth import get_user_model

from apps.skill.models import Skill

User = get_user_model()


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+")
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True)
    resume = models.FileField(upload_to="profile_resume")
    portfolio = models.URLField(max_length=200, blank=True)
    skills = models.ManyToManyField(Skill)

    def __str__(self) -> str:
        return f"{self.user} Profile"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
