# Django imports
from django.urls import path

# Third-part library imports
from rest_framework.routers import DefaultRouter

# Local modules imports
from activities import views, generat_mock_activities

app_name = "activities"
router = DefaultRouter()

urlpatterns = [

    
    # --------------------------------- Endpoints -------------------------------- #
    #! Admin Dashboard
    path('all_activities/', views.AllActivities.as_view()),
    path('create_activity/', views.CreateActivity.as_view()),
    path('rud_activities/<int:pk>', views.AdminRUDActivities.as_view()),
    path('calender/', views.ActivityByMonthAPIView.as_view()),
    
    
    
    
    
    path('mock_activities/', generat_mock_activities.create_mock_activities),
    
    path('test/', views.TestActi.as_view()),
    
    
    #!landing page
    path('upcoming_activities/', views.UpcomingActivities.as_view()),
    path('past_activities/', views.PastActivities.as_view()),
    path('activity_details/<int:pk>', views.activity_details),
    path('activity_by_type/', views.activity_by_type),
    path('activity_by_name/', views.activity_by_name),
    path('activity_by_location/', views.activity_by_location),
    
    
    
    
    
    
    # --------------------------------- End Endpoints -------------------------------- #
    
]
