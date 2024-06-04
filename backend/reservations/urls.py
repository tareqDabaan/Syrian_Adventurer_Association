from django.urls import path
from reservations import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'approvals', views.RequestViewSet, basename='reservation')
app_name = "reservations"

urlpatterns = [

    path('api/user/<int:user_id>/activity-count/', views.ActivityCountAPIView.as_view(), name='activity_count_api'),


    # ------------------------------- Admin Actions ------------------------------ #
    path('list_pending_requests/',  views.RequestViewSet.as_view({'get': 'list_pending_requests'}), name='pending-requests'),
    path('approve/<int:pk>/',  views.RequestViewSet.as_view({'post': 'approve_request'}), name='approve'),
    path('reject/<int:pk>/',   views.RequestViewSet.as_view({'post': 'reject_request'}), name='reject'),

]
