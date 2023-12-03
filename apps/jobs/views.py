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

    def get(self, request, uuid):
        job = JobListing.objects.get(id=uuid)
        serializer = JobSerializer(job)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        job = JobListing.objects.get(id=uuid)
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        job = JobListing.objects.get(id=uuid)
        job.delete()
        return response.Response()


class CreateJob(views.APIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the 'user' field to the authenticated user
            serializer.validated_data["user"] = request.user
            # Create the vendor instance
            serializer.save()
            # You can perform additional actions here if needed
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
