# Django imports
from django.urls import path

# Third-part library imports
from rest_framework.routers import DefaultRouter

# Local modules imports
from admins import views
from activities.views import activity_by_name
app_name = "admins"

urlpatterns = [

    
    # --------------------------------- Endpoints -------------------------------- #
    #! Admin Dashboard Filters
    path('member_by_name/', views.member_by_name),
    path('article_by_name/', views.article_by_name),
    path('reservation_by_email/', views.reservation_by_user_email),
    path('user_by_name/', views.user_by_name),
    path('activity_by_name/', activity_by_name),
    
    
    path('contact_us/', views.ContactUs.as_view({'post':'send_message'}), name='send_message'),
    path('list_messages/', views.ContactUs.as_view({'get':'list_messages'}), name='list_messages'),
    path('message_details/<int:pk>/', views.ContactUs.as_view({'get':'message_details'}), name='list_messages'),
    path('admin_response/<int:pk>/', views.ContactUs.as_view({'post':'admin_response'}), name='list_messages'),
    
    
    
    
    #! Statistics
    path('total_users/', views.Statistics.as_view({"get":"get_total_users"})),
    path('new_users/', views.Statistics.as_view({"get":"get_new_users_over_time"})),
    path('total_activities/', views.Statistics.as_view({"get":"total_activities"})),
    path('past_activities_per_city/', views.Statistics.as_view({"get":"past_activities"})),
    path('past_activities_per_month/', views.Statistics.as_view({"get":"past_activities_by_month"})),
    
    path('users_city/', views.user_counts_by_location), #Used in dashboard
    
    path('count_users/', views.Statistics.as_view({"get":"count_users"})),
    
    path('count_activities/', views.Statistics.as_view({"get":"count_activities"})),
    
    
    # --------------------------------- End Endpoints -------------------------------- #
    
]
