# Django imports
from django.urls import path, include

# Third-part library imports
from rest_framework.routers import DefaultRouter

# Local modules imports
from gallery import views

app_name = "gallery"
router = DefaultRouter()
router.register('', views.GalleryViewSet)

urlpatterns = [

    
    # --------------------------------- Endpoints -------------------------------- #
    path('list/', include(router.urls)),
    path('upload/', views.GalleryUploadAPI.as_view()),
    path('delete/<int:pk>/', views.GalleryDeleteView.as_view(), name='delete_gallery'),  # Add a name for clarity
    # --------------------------------- End Endpoints -------------------------------- #
    
]
