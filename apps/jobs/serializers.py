from rest_framework import serializers


from .models import CandidacyApplication, JobListing


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = "__all__"


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidacyApplication
        fields = ("proposal_resume", "job")


# Validation on serializers
