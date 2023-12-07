from rest_framework import views, response, status
from django.db.models import Q
from .models import SavedSearch, Notification
from apps.jobs.models import JobListing  # Import your JobListing model
from .serializers import SavedSearchSerializer, NotificationSerializer
from django.core.mail import send_mail
from django.conf import settings


class SaveSearchView(views.APIView):
    def post(self, request):
        serializer = SavedSearchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSavedSearchesView(views.APIView):
    def get(self, request):
        saved_searches = SavedSearch.objects.filter(user=request.user)
        serializer = SavedSearchSerializer(saved_searches, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class JobNotificationView(views.APIView):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        saved_searches = SavedSearch.objects.filter(user=request.user)

        matching_jobs = JobListing.objects.none()

        for saved_search in saved_searches:
            # Construct filter conditions based on the saved search criteria
            filter_conditions = Q()

            if saved_search.location:
                filter_conditions &= Q(address__icontains=saved_search.location)
            if saved_search.job_type:
                filter_conditions &= Q(job_type=saved_search.job_type)
            if saved_search.industry:
                filter_conditions &= Q(industry=saved_search.industry)
            # Add more conditions as needed

            # Apply the filter conditions to get matching jobs
            matching_jobs |= JobListing.objects.filter(filter_conditions)

        for job in matching_jobs:
            Notification.objects.create(user=request.user, job=job)

            # Send email notification (replace with your email sending logic)
            send_mail(
                "New Matching Job Notification",
                f"There is a new job matching your saved search: {job.title}",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

        return response.Response(status=status.HTTP_201_CREATED)
