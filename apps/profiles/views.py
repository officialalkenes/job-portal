from django.shortcuts import get_object_or_404, render
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import response, status, permissions, views

from .serializers import FreelancerProfile, FreelancerProfileSerializer


class UpdateProfileView(views.APIView):
    serializer_class = FreelancerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request):
        user_profile = get_object_or_404(FreelancerProfile, user=request.user)
        serializer = FreelancerProfileSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UploadResumeView(views.APIView):
#     serializer_class = FreelancerProfile
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def post(self, request):
#         ...
