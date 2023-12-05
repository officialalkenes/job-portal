from django_filters import rest_framework as filters

from .models import JobListing


class JobFilterset(filters.FilterSet):
    keywords = filters.CharFilter(field_name="title", lookup_expr="icontains")
    location = filters.CharFilter(field_name="address", lookup_expr="icontains")
    min_salary = filters.NumberFilter(field_name="salary" or 0, lookup_expr="gte")
    max_salary = filters.NumberFilter(field_name="salary" or 1000000, lookup_expr="lte")

    class Meta:
        model = JobListing
        fields = (
            "keyword",
            "location",
            "company",
            "job_type",
            "work_type",
            "education",
            "experience",
            "min_salary",
            "max_salary",
        )
