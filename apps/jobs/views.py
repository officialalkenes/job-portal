from django.shortcuts import render

from rest_framework import authentication, permissions, response, status, views
from .serializers import JobSerializer


class AllJobs(views.APIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
