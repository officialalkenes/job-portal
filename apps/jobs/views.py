from django.shortcuts import render

from django.db.models import Aggregate, Avg, Count, Min, Max, Sum

from rest_framework import (
    pagination,
    permissions,
    response,
    status,
    views,
)

from apps.jobs.filters import JobFilterset
from .serializers import JobSerializer
from .models import JobListing


class AllJobs(views.APIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    # authentication_classes = [JWTAuthentication]

    def get(self, request):
        filterset = JobFilterset(
            request.GET, queryset=JobListing.objects.all().order_by("-created")
        )
        total_qs = filterset.qs.count()
        paginated_response = 5
        paginator = pagination.PageNumberPagination()
        paginator.page_size = paginated_response
        queryset = paginator.paginate_queryset(filterset.qs, request)

        serializer = JobSerializer(queryset, many=True)
        return response.Response(
            {
                "total_qs_count": total_qs,
                "jobs": serializer.data,
                "paginated_response": paginated_response,
            }
        )


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
            if request.user != job.user:
                return response.Response(
                    {"messages": "You are not Authorized to update this Job"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        job = JobListing.objects.get(id=uuid)
        if request.user != job.user or not request.user.is_superuser:
            return response.Response(
                {"messages": "You are not Authorized to delete this Job"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        job.delete()
        return response.Response(
            {"message": "user deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


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


class GetJobStat(views.APIView):
    serializer = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, topic):
        topics = {"topic__icontains": topic}
        jobs = JobListing.objects.filter(**topics)
        if len(jobs) == 0:
            return response.Response({"message": f"No stats found for {topic}"})
        # stats = jobs.aggregate(total_jobs=Count("title"))
