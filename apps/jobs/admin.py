from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import JobListing


@admin.register(JobListing)
class JobListingAdmin(OSMGeoAdmin):
    list_display = (
        "title",
        "company",
        "job_type",
        "education",
        "experience",
        "salary",
    )
    list_filter = (
        "job_type",
        "education",
        "experience",
    )
    search_fields = (
        "title",
        "company",
        "description",
    )
