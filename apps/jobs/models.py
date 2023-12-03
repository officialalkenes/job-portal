import uuid
import geocoder

from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.gis.db import models as modelsgis
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator

from decouple import config
from .validators import validate_positions

User = get_user_model()


class JobType(models.TextChoices):
    Permanent = "Permanent"
    Remote = "Remote"
    Contract = "Contract"
    Internship = "InternShip"


class EducationLevel(models.TextChoices):
    Bachelors = "Bachelors"
    Masters = "Masters"
    Phd = "Phd"


class Industry(models.TextChoices):
    IT = "Information and Technology"
    AI = "Ai Services"
    Education = "Education"
    Comms = "Telecommunication"
    Development = "Software Development"
    Design = "Creative Designs"
    Support = "Admin/Customer Support"
    Sales = "Marketting and Sales"


class ExperienceChoice(models.TextChoices):
    INEXPERIENCE = "No Experience"
    LESS_THAN_A_YEAR = "Less than 1 year"
    ONE_YEAR = "One Year"
    TWO_YEARS = "Two Years"
    ABOVE_TWO_YEARS = "Two Years and above"


class WorkPlaceTypes(models.TextChoices):
    ONSITE = "On Site"
    HYBRID = "Hybrid"
    REMOTE = "Remote"


class JobListing(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, verbose_name="Job Title")
    description = models.TextField(null=True)
    company = models.CharField(max_length=100)
    company_email = models.EmailField(null=True)
    location = models.CharField(
        max_length=255, null=True, verbose_name=_("Job Location")
    )
    job_type = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.Remote
    )
    work_type = models.CharField(
        max_length=100, choices=WorkPlaceTypes.choices, default=WorkPlaceTypes.ONSITE
    )
    education = models.CharField(max_length=30, choices=EducationLevel.choices)
    experience = models.CharField(max_length=30, choices=ExperienceChoice.choices)
    salary = models.PositiveIntegerField(
        default=5, validators=[MinValueValidator(5), MaxValueValidator(1000_000_000)]
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    application_link = models.URLField(blank=True)
    geo_point = modelsgis.PointField(default=Point(0.0, 0.0), blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        key_geo = config("GEOCODING_KEY")
        g = geocoder.mapquest(self.location, key=key_geo)
        longitude = g.lng
        latitude = g.lat
        self.country = g.country
        self.city = g.city
        self.geo_point = Point(longitude, latitude)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"
