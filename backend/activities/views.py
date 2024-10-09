# Third-part library imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.decorators import api_view
from activities.pagination import CustomPageNumberPaginator
from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import Distance

# Local modules imports
from activities.serializers import *
from activities.models import Activity

# Django imports
from django.utils import timezone
from django.http import HttpRequest
from urllib.parse import unquote
from datetime import date


# * ---------------------------- For Admin Dashboard --------------------------- #

class TestActi(generics.ListAPIView):
    serializer_class = DeleteSerializer
    queryset = Activity.objects.all()


class AllActivities(generics.ListAPIView):
    """
    API endpoint to retrieve a paginated list of all activities.
    **Permissions:** Allowed for admins only (GET).
    **HTTP Method:** GET
    **Pagination:** Uses `PageNumberPagination` for efficient handling of large datasets.
    **Response:**
        - A paginated list of activities serialized using the `ActivitySerializer`.


    - To retrieve the first page with a default page size (e.g., 10):
        - No additional parameters needed.

    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    # permission_classes = (permissions.IsAdminUser, )
    pagination_class = CustomPageNumberPaginator
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.values('id', 'activity_name', 'location',
                               'start_at__date', 'activity_type__activity_type')
        page = self.paginate_queryset(data)
        if page is not None:
            response_data = []

            for item in page:
                # to remove the old key retrieve its value then assign this value to a new key
                item['start_at'] = item.pop('start_at__date')
                item['activity_type'] = item.pop('activity_type__activity_type')
                response_data.append(item)

            return self.get_paginated_response(response_data)

        data = queryset.values('id', 'activity_name', 'location',
                               'start_at__date', 'activity_type__activity_type')

        response_data = []

        for item in data:
            item['start_at'] = item.pop('start_at__date')
            item['activity_type'] = item.pop('activity_type__activity_type')
            response_data.append(item)

        return Response(response_data)


class CreateActivity(generics.CreateAPIView):
    """
    API endpoint for admins to create a new activity.
    **Permissions:** Allowed for admins only (POST).
    **HTTP Method:** POST
    **Request Body:** Provide data for the new activity according to the `CreateActivitySerializer` fields.

    """
    queryset = Activity.objects.all()
    serializer_class = CreateActivitySerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AdminRUDActivities(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for admins to retrieve, update, or delete an activity by its ID.

    **Permissions:** Allowed for admins only (GET, PUT, DELETE).

    **HTTP Methods:**
        - GET: Retrieve an activity by its ID.
        - PUT: Update an existing activity.
        - DELETE: Delete an activity.

    **URL Path Parameter:**
        - activity_id: The primary key of the activity to be retrieved, updated, or deleted.

    **Response:**
        - On success (GET, PUT): Serialized data of the retrieved or updated activity.
        - On success (DELETE): HTTP 204 No Content.
        - On error (all methods): Appropriate error response with status code.

    **
    """
    queryset = Activity.objects
    serializer_class = RUDActivitySerializer
    # permission_classes = (permissions.IsAdminUser,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Edit
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an activity.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.http import JsonResponse

class ActivityByMonthAPIView(APIView):
    """
    This API endpoint to retrieve activity names and dates for a specified year and month.
    127.0.0.1:8000/activities/calender?year=y&month=m 
    """
    
    # permission_classes = (permissions.IsAdminUser,)
    
    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    def get(self, request, format=None):

        try:
            starting_str = request.GET.get('starting_at')
            ending_str = request.GET.get('ending_at')

            try:
                starting_date = date.fromisoformat(starting_str)
                ending_date = date.fromisoformat(ending_str)

            except (ValueError, TypeError):
                raise ValueError(
                    'Invalid starting or ending date format (YYYY-MM-DD)')

            # ? Check that the sent month is valid
            if starting_date > ending_date:
                raise ValueError(
                    'Starting date must be before or equal to ending date')

            # ? Query, return activities filtered
            activities = Activity.objects.filter(
                start_at__gte=starting_str,
                start_at__lte=ending_str
            ).values('activity_name', 'start_at')

            if not activities:
                response = Response({
                    'details': f'No activities found between {starting_str} and {ending_str}'
                },  status=status.HTTP_204_NO_CONTENT)
                response['Access-Control-Allow-Origin'] = '*'
                return response

            response_data = [
                {
                    'title': activity['activity_name'],
                    'date': activity['start_at'].strftime('%Y-%m-%d')
                }
                for activity in activities
            ]

            response = Response(response_data, status=status.HTTP_200_OK)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        except (ValueError, KeyError):
            response = Response({'error': 'Invalid year or month parameter'}, status=status.HTTP_400_BAD_REQUEST)
            response['Access-Control-Allow-Origin'] = '*'
            return response

        except Exception:
            response = Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response['Access-Control-Allow-Origin'] = '*'
            return response

# * ---------------------------- End Admin Dashboard --------------------------- #


# ------------------------------- Landing Page + Activities Page------------------------------- #
class UpcomingActivities(generics.ListAPIView):
    #! Landing Page
    """
    This API is used to return the upcoming activities which will be displayed
    in the landing page.
    It returns: Id, Image, Name, Location, Start_Date, End_Date, Type
    """
    serializer_class = UpComingActivitySerializerLimited
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return Activity.objects.filter(start_at__gte=timezone.now())


# ------------------------------ Activities Page ----------------------------- #
class PastActivities(generics.ListAPIView):
    #! Landing Page
    """
    This API is used to return the past activities which will be displayed
    in the landing page.
    It returns: Id, Image, Name, Location, Start_Date, End_Date, Type
    """
    serializer_class = UpComingActivitySerializerLimited
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return Activity.objects.filter(start_at__lte=timezone.now())


# -------------------- Activity Details Page ( The Peak ) -------------------- #
@api_view(['GET'])
def activity_details(request: HttpRequest, pk=None):
    """
    This API is used to return a specific activity via the ID to be displayed
    in the landing page.
    """
    try:
        activity = Activity.objects.get(pk=pk)
        serializer = ActivityDetailsSerializer(activity)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Activity.DoesNotExist:
        return Response({
            "details": "Activity not found"

        }, status=status.HTTP_404_NOT_FOUND)


# -------------------- Special Activity Page ( Hiking or Camping ) -------------------- #
@api_view(['GET'])
def activity_by_type(request: HttpRequest):
    #! Desktop 15
    # TODO Make it for capital and small
    """
    This API is used to return the upcoming activities which will be displayed
    in the Activities page.
    Send the activity_type as a query_params 
    """
    activity_type = request.query_params.get("activity_type")

    if not activity_type:
        return Response({
            'error': 'activity_type is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    activities = Activity.objects.filter(
        activity_type__activity_type__icontains=activity_type)

    if not activities.exists():
        return Response({
            'message': f'No upcoming events found for type "{activity_type}".'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UpComingActivitySerializerLimited(activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------- Filters --------------------------------- #
@api_view(['GET'])
def activity_by_name(request: HttpRequest):
    """
    This API will return activities filtered by the activity name
    Send the name via params splited with _ 
    127.0.0.1:8000/activities/activity_by_name?activity_name=(activity name) 
    """
    try:
        # Extract the activity name from the params
        activity_name = request.query_params.get('activity_name')
        # Decode the URL-encoded activity name
        decoded_activity_name = unquote(activity_name)
        text_seq = decoded_activity_name.split("_")  # Split the activity_name string
        # Filter activities based on the first part of the split name
        activities = Activity.objects.filter(
            activity_name__istartswith=text_seq[0])

        if not activity_name:
            return Response({
                'error': 'activity_name is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not activities.exists():
            return Response({
                "error": "Activity not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ActivityFilterSerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response("An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def activity_by_location(request: HttpRequest):
    """
    This API will return activities filtered by the activity location
    Send the location capital
    127.0.0.1:8000/activities/activity_by_name?activity_location=(activity location) 
    """
    activity_location = request.query_params.get('location')  # Extract the activity location from the params

    if not activity_location:
        return Response({
            'error': 'location parameter is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    activities = Activity.objects.filter(location__icontains=activity_location)

    if not activities.exists():
        return Response({
            "error": "Activity not found"
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = UpComingActivitySerializerLimited(activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

