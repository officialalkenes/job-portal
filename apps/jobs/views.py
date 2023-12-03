from django.shortcuts import render

from rest_framework import authentication, permissions, response, status, views
from .serializers import JobSerializer
from .models import JobListing


class AllJobs(views.APIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        jobs = JobListing.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return response.Response(serializer.data)


class GetUpdateJob(views.APIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        job = JobListing.objects.get(id=id)
        serializer = JobSerializer(job)
        return response.Response(serializer, status=status.HTTP_200_OK)

    def update(self, request, id):
        job = JobListing.objects.get(id=id)
        serializer = JobSerializer(job, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer, status=status.HTTP_200_OK)
