from typing import Optional
from django import forms

from .models import FreelancerProfile


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = "__all__"
