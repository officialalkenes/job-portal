import geocoder

from django.contrib.auth import get_user_model
from django.db import models

from django.contrib.gis.db import models as modelsgis
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator

from decouple import config


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


class JobListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100, verbose_name="Job Title")
    description = models.TextField(null=True)
    company_email = models.EmailField(null=True)
    address = models.CharField(max_length=255, null=True)
    job_type = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.Remote
    )
    education = models.CharField(max_length=20, choices=EducationLevel.choices)
    industry = models.CharField(max_length=20, choices=Industry.choices)
    experience = models.CharField(max_length=20, choices=ExperienceChoice.choices)
    salary = models.PositiveIntegerField(
        default=5, validators=[MinValueValidator(5), MaxValueValidator(1000_000)]
    )
    positions = models.CharField(max_length=100)
    geo_point = modelsgis.PointField(default=Point(0.0, 0.0))
    company = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        key_geo = config("GEOCODING_KEY")
        g = geocoder.mapquest(self.address, key=key_geo)
        longitude = g.lng
        latitude = g.lat
        self.geo_point = Point(longitude, latitude)
        return super().save(*args, **kwargs)
