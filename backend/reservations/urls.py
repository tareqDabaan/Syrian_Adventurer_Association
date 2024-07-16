from django.urls import path
from reservations import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'approvals', views.RequestViewSet, basename='reservation')
app_name = "reservations"

urlpatterns = [

    path('activities_count/<int:user_id>/', views.Statistics.as_view({'get':'get_activity_counts'}), name='activity_count_api'),

    # ------------------------------- Admin Actions ------------------------------ #
    path('create_request/', views.RequestViewSet.as_view({'post': 'create_request'}), name='create'),
    path('list_pending_requests/', views.RequestViewSet.as_view({'get': 'list_pending_requests'}), name='pending-requests'),
    path('list_accepted_requests/', views.RequestViewSet.as_view({'get': 'list_accepted_requests'}), name='approved-requests'),
    path('list_rejected_requests/', views.RequestViewSet.as_view({'get': 'list_rejected_requests'}), name='rejected-requests'),
    path('approve/<int:pk>/', views.RequestViewSet.as_view({'post': 'approve_request'}), name='approve'),
    path('reject/<int:pk>/', views.RequestViewSet.as_view({'post': 'reject_request'}), name='reject'),

    # -------------------------------- Testing Map ------------------------------- #
    path('map_details/', views.get_activity_details, name='map_details'),

    # ------------------------------ Testing payment ----------------------------- #
    path('payment/<int:reservation_id>/', views.payment_page, name='payment_page'),
    path('process_mock_payment/', views.process_mock_payment, name='process_mock_payment'),
]

urlpatterns += router.urls
