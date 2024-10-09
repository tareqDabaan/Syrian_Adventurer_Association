import csv
from django.http import HttpResponse

import random

from rest_framework.decorators import api_view

from rest_framework.response import Response
from .models import Dataset

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from rest_framework.generics import GenericAPIView


@api_view(['POST'])
def create_mock_preferences(request):
    try:
        n = request.data.get('n', 5)

        budget = (200000, 500000)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        places = ["Lattakia", "Tartus", "Homs", "Mashqita", "Alqadmus", "Safita", "Kafroun", "Maloula", "Slunfa", "Kasab"]
        types = ["Hiking", "Camping"]
        difficulties = ["Easy", "Medium", "Hard"]

        for _ in range(n):
            budget = round(random.randrange(85000,300000))
            preferred_month = random.choice(months)
            preferred_places = random.choice(places)
            preferred_types = random.choice(types)
            preferred_difficulity = random.choice(difficulties)
            more_than_day = False if preferred_types == "Hiking" else random.choice([True, False])

            Dataset.objects.create(
                budget=budget,
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


class RecommendationAPIView(GenericAPIView):

    def get(self, request):
        data = Dataset.objects.all().values()
        df = pd.DataFrame(list(data.values()))

        # Normalize the budget in reverse (so that lower values get higher normalized values)
        scaler_budget = MinMaxScaler()
        df['budget_normalized'] = scaler_budget.fit_transform(df[['budget']])
        df['budget_normalized'] = 1 - df['budget_normalized']

        # Encode categorical data
        label_encoders = {}
        categorical_columns = ['preferred_month', 'preferred_places', 'preferred_types', 'preferred_difficulity']
        for col in categorical_columns:
            le = LabelEncoder()
            df[col + '_encoded'] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le

        # Encode boolean data
        df['more_than_day_encoded'] = df['more_than_day'].astype(int)

        # Create Decision Matrix
        criteria_columns = ['budget_normalized', 'preferred_month_encoded', 'preferred_places_encoded',
                            'preferred_types_encoded', 'preferred_difficulity_encoded', 'more_than_day_encoded']
        decision_matrix = df[criteria_columns].values

        # Assuming maximum weight for minimum budget
        weights = np.array([0.3, 0.1, 0.1, 0.3, 0.1, 0.1])  

        # Normalize the decision matrix
        scaler = MinMaxScaler()
        normalized_matrix = scaler.fit_transform(decision_matrix)

        # Weight the normalized matrix
        weighted_matrix = normalized_matrix * weights

        ideal_solution = np.max(weighted_matrix, axis=0)
        negative_ideal_solution = np.min(weighted_matrix, axis=0)

        distance_to_ideal = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1)) #!! GPT
        distance_to_negative_ideal = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1)) #!!

        # Calculate the TOPSIS score
        topsis_score = distance_to_negative_ideal / (distance_to_ideal + distance_to_negative_ideal)

        df['topsis_score'] = topsis_score

        # Order the DataFrame by TOPSIS scores in descending order
        df_sorted = df.sort_values('topsis_score', ascending=False)

        recommended_activities = []
        for index, row in df_sorted.iterrows():
            activity = {
                "activity_type": row['preferred_types'],
                "location": row['preferred_places'],
                "month": row['preferred_month'],
                "difficulty": row['preferred_difficulity'],
                "budget": row['budget'],
                "days": row['more_than_day']
            }
            recommended_activities.append(activity)

        return Response({"recommended_activities": recommended_activities})