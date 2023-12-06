from rest_framework import serializers


from .models import CandidacyApllication, JobListing


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = "__all__"


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidacyApllication
        fields = ("proposal_resume", "job")


# Validation on serializers
