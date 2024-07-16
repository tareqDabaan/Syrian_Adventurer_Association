from rest_framework.response import Response
from rest_framework import status,viewsets, permissions, generics
from rest_framework.decorators import permission_classes, api_view
from user_preferences import serializers
from .models import Preferences
from .utils import generate_csv_response
import pandas as pd

class PreferenceListCreate(generics.ListCreateAPIView):
    queryset = Preferences.objects.all()
    serializer_class = serializers.UserPreferencesSerializer

    
class ActivityPreferenceStatistics(generics.GenericAPIView):
    serializer_class = serializers.UserPreferencesSerializer

    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)

        stats = {
            "average_price_min": df["preferred_price_min"].mean(),
            "average_price_max": df["preferred_price_max"].mean(),
            "most_preferred_month": df["preferred_month"].mode()[0],
            "most_preferred_place": df["preferred_places"].mode()[0],
            "most_preferred_type": df["preferred_types"].mode()[0],
            "most_preferred_difficulty": df["preferred_difficulity"].mode()[0],
            "percentage_of_people_prefer_more_than_day": df["more_than_day"].mean() * 100,
        }
        counts = {
                    "preferred_month_counts": df["preferred_month"].value_counts().to_dict(),
                    "preferred_places_counts": df["preferred_places"].value_counts().to_dict(),
                    "preferred_types_counts": df["preferred_types"].value_counts().to_dict(),
                    "preferred_difficulty_counts": df["preferred_difficulity"].value_counts().to_dict(),
                    "more_than_a_day_counts": df["more_than_day"].value_counts().to_dict(),
                }
        
        result = {**stats, **counts}
        
        return Response(result)
        
        
# @permission_classes([permissions.IsAdminUser])
@api_view(['GET'])
def generate_reports(request, *args, **kwargs):
    preferences = Preferences.objects.all()
    return generate_csv_response(preferences)


# import matplotlib.pyplot as plt
# import seaborn as sns
# import io
# from django.http import HttpResponse

# class ActivityPreferenceVisualization(generics.GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         data = Preferences.objects.all().values()
#         df = pd.DataFrame(data)

#         plt.figure(figsize=(10, 6))
#         sns.countplot(x='preferred_month', data=df)
#         plt.title('Preferred Activities by Month')

#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         plt.close()
#         buf.seek(0)
#         return HttpResponse(buf, content_type='image/png')


class ActivityPreferenceSegmentation(generics.GenericAPIView):
    serializer_class = serializers.UserPreferencesSerializer

    def get(self, request, *args, **kwargs):
        data = Preferences.objects.all().values()
        df = pd.DataFrame(data)

        segments = {
            "budget_travelers": df[(df["preferred_price_max"] <= 100)].to_dict('records'),
            "luxury_travelers": df[(df["preferred_price_min"] >= 500)].to_dict('records'),
            "adventure_seekers": df[df["preferred_types"].str.contains("Hiking|Camping")].to_dict('records'),
        }

        return Response(segments)
