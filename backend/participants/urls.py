from django.urls import path
from participants import views

app_name = 'participants'
urlpatterns = [
    path('api/activity/<int:activity_id>/price/', views.get_activity_price, name='get_activity_price'),
]
