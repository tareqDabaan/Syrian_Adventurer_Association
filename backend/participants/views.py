# pricing/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import get_dynamic_price
from activities.models import Activity

@api_view(['GET'])
def get_activity_price(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        price = get_dynamic_price(activity_id)
        if price is not None:
            return Response({'activity_name': activity.activity_name, 'dynamic_price': price})
        else:
            return Response({'error': 'Failed to predict price'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=status.HTTP_404_NOT_FOUND)
