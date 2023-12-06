from rest_framework import serializers

from .models import FreelancerProfile


class FreelancerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreelancerProfile
        exclude = ("user",)
