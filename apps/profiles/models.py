from django.db import models

from django.contrib.auth import get_user_model

from skill.models import Skill

User = get_user_model()


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+")
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True)
    skills = models.CharField(max_length=200, blank=True)
    portfolio = models.URLField(max_length=200, blank=True)
    reviews = models.ManyToManyField(
        User, through="Review", related_name="reviews_received"
    )
    ratings = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    skill = models.ManyToManyField()

    def __str__(self) -> str:
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_reviews(self):
        return self.reviews.all()

    def get_ratings(self):
        return self.ratings
