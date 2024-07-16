from django.urls import path, include
from user_preferences import views, utils
from rest_framework.routers import DefaultRouter
from members import generate_mock_members

app_name = "members"

urlpatterns = [
    path('generate_reports/', views.generate_reports, name='generate_reports'),
    path('list_create_preferences/', views.PreferenceListCreate.as_view(), name='preferences'),
    path('statistics/', views.ActivityPreferenceStatistics.as_view(), name='statistics'),
    path('segmentation/', views.ActivityPreferenceSegmentation.as_view(), name='segmentation'),
    
    
    path('mock/', utils.create_mock_preferences, name='create-mock-preferences'),

]