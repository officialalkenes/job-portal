from rest_framework import serializers


from .models import JobListing


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = "__all__"
