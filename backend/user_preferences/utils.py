import csv
from django.http import HttpResponse

from datetime import datetime
import random

from rest_framework.decorators import permission_classes, api_view

from rest_framework.response import Response
from .models import Preferences

@api_view(['POST'])
def create_mock_preferences(request):
    try:
        n = request.data.get('n', 5)

        price_min_range = (100, 100)
        price_max_range = (1000, 10000)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        places = ["Lattakia", "Tartus", "Yosemite Park", "Amazon Rainforest", "Nile River"]
        types = ["Hiking", "Camping"]
        difficulties = ["Easy", "Medium", "Hard"]

        for _ in range(n):
            preferred_price_min = round(random.uniform(*price_min_range), 2)
            preferred_price_max = round(random.uniform(preferred_price_min, price_max_range[1]), 2)
            preferred_month = random.choice(months)
            preferred_places = random.choice(places)
            preferred_types = random.choice(types)
            preferred_difficulity = random.choice(difficulties)
            more_than_day = random.choice([True, False])

            Preferences.objects.create(
                preferred_price_min=preferred_price_min,
                preferred_price_max=preferred_price_max,
                preferred_month=preferred_month,
                preferred_places=preferred_places,
                preferred_types=preferred_types,
                preferred_difficulity=preferred_difficulity,
                more_than_day=more_than_day
            )

        return Response({"message": "Mock preferences created successfully."}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
def generate_csv_response(preferences_queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_preferences.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Preferred Price Min', 'Preferred Price Max', 'Preferred Month',
        'Preferred Places', 'Preferred Types', 'Preferred Difficulty', 'More Than a Day'
    ])

    for pref in preferences_queryset:
        writer.writerow([
            pref.id, pref.preferred_price_min, pref.preferred_price_max, pref.preferred_month,
            pref.preferred_places, pref.preferred_types, pref.preferred_difficulity, pref.more_than_day
        ])

    return response
