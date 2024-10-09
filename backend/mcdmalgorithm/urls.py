from django.urls import path, include
from rest_framework.routers import DefaultRouter
from members import generate_mock_members
from mcdmalgorithm import views
app_name = "mcdmalgorithm"


urlpatterns = [
    
    path('mock/', views.create_mock_preferences, name='create-mock-preferences'),
    
    path('rec/', views.RecommendationAPIView.as_view(), name='create-mock-preferences'),
    
]