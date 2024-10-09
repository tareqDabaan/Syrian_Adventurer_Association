from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from user_preferences import serializers
from .models import Preferences
from .utils import generate_csv_response
import pandas as pd

import pickle
import os

import random


class PreferenceListCreate(generics.ListCreateAPIView):
    """
    List and create the user's preferences
    """
    queryset = Preferences.objects.all()
    serializer_class = serializers.UserPreferencesSerializer
    
class PreferredMonthCounts(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)
        preferred_month_counts = df["preferred_month"].value_counts().to_dict()
        
        return Response({"preferred_month_counts": preferred_month_counts})
    
    
class PreferredPlacesCounts(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)
        preferred_places_counts = df["preferred_places"].value_counts().to_dict()
        
        return Response({"preferred_places_counts": preferred_places_counts})
    
class TopMonths(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)
        top_months = df["preferred_month"].value_counts().head(3).to_dict()
        
        return Response({"top_months": top_months})
    
class TopPlaces(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)
        top_places = df["preferred_places"].value_counts().head(3).to_dict()
        
        return Response({"top_places": top_places})


class ActivityPreferenceStatistics(generics.GenericAPIView):
    """
    List user's preferences as statistics for better visualization
    """
    serializer_class = serializers.UserPreferencesSerializer

    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)
        stats = {
            "average_price_min": round(df["preferred_price_min"].mean()),
            "average_price_max": round(df["preferred_price_max"].mean()),
            "most_preferred_month": df["preferred_month"].mode()[0],
            "most_preferred_place": df["preferred_places"].mode()[0],
            "most_preferred_type": df["preferred_types"].mode()[0],
            "most_preferred_difficulty": df["preferred_difficulity"].mode()[0],
            "percentage_of_people_prefer_more_than_day": round(df["more_than_day"].mean() * 100),
        }
        
        counts = {
                    "preferred_month_counts": df["preferred_month"].value_counts().to_dict(),
                    "preferred_places_counts": df["preferred_places"].value_counts().to_dict(),
                    "preferred_types_counts": df["preferred_types"].value_counts().to_dict(),
                    "preferred_difficulty_counts": df["preferred_difficulity"].value_counts().to_dict(),
                    "more_than_a_day_counts": df["more_than_day"].value_counts().to_dict(),
                }
        
        top_months = df["preferred_month"].value_counts().head(3).to_dict()
        top_places = df["preferred_places"].value_counts().head(3).to_dict()
        top_types = df["preferred_types"].value_counts().head(3).to_dict()
        
        insights = {
            "top_months": top_months,
            "top_places": top_places,
            "top_types": top_types
        }

        result = {**stats, **counts, **insights}
        
        return Response(result)
        
        
# @permission_classes([permissions.IsAdminUser])
@api_view(['GET'])
def generate_reports(request, *args, **kwargs):
    """
    Allow admins to generate the data as CSV files
    """
    preferences = Preferences.objects.all()
    return generate_csv_response(preferences)


class RecommendActivities(generics.GenericAPIView):
   
    def calculate_average_price(self, min_price, max_price):
        """Calculate average price between min and max."""
        return (min_price + max_price) / 2
    
    def determine_days(self, days_counts):
        """
        Determine whether more people prefer activities lasting more than a day or not.
        """
        true_count = days_counts.get(True, 0)
        false_count = days_counts.get(False, 0)
        
        if true_count > false_count:
            return 'more than a day'
        elif false_count > true_count:
            return 'one day'
        
    def get(self, request, *args, **kwargs):
        # Get stats from the API
        stats_response = ActivityPreferenceStatistics().get(request).data

        # Simple rule-based recommendation based on stats
        recommended_activities = []
        
        # Extract the data needed for recommendations with defaults
        top_types = stats_response.get("top_types", {})
        top_places = stats_response.get("top_places", {})
        top_months = stats_response.get("top_months", {})
        min_price = stats_response.get("average_price_min", 0)
        max_price = stats_response.get("average_price_max", 0)
        days_counts = stats_response.get("more_than_a_day_counts", {})
        
        if not (top_types and top_places and top_months):
            return Response({"recommended_activities": []}, status=204)  # No content

        recommended_activities.append({
            "activity_type": list(top_types.keys())[0],
            "location": list(top_places.keys())[0],
            "month": list(top_months.keys())[0],
            "price_range": f"{min_price:.2f} - {max_price:.2f}",
            "days": self.determine_days(days_counts),
            "average_recommended_price": self.calculate_average_price(min_price, max_price),
            "suggestion": "Create a new activity with this type, location, month, and optimal price range"
        })
        
        return Response({"recommended_activities": recommended_activities})
