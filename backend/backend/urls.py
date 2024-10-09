
from django.contrib import admin
from django.http import HttpResponse

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import(TokenObtainPairView, TokenRefreshView,)


def index(request):
    return HttpResponse("Hello, world. You're at the root index.")

urlpatterns = [
    
    path('', index),  # Root URL

    # Admin Site 
    path('admin/', admin.site.urls),
    
    # JWT endpoints 
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    
    # Users Application Endpoints 
    path('auth/', include('users.urls', namespace = 'users')),

    # Members Application Endpoints 
    path('members/', include('members.urls', namespace = 'members')),    
    
    # Activities Application Endpoints 
    path('activities/', include('activities.urls', namespace = 'activities')),    
    
    # Articles Application Endpoints 
    path('articles/', include('articles.urls', namespace = 'articles')),    
    
    # Gallery Application Endpoints 
    path('gallery/', include('gallery.urls', namespace = 'gallery')),    
    
    # Reservations Application Endpoints 
    path('reservations/', include('reservations.urls', namespace = 'reservations')),  
    
    # Admins Application Endpoints 
    path('admins/', include('admins.urls', namespace = 'admins')),  
    
    # User Preferences Application Endpoints 
    path('preferences/', include('user_preferences.urls', namespace = 'user_preferences')),  
   
    # User Preferences Application Endpoints 
    path('mcdm/', include('mcdmalgorithm.urls', namespace = 'mcdm')),  
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
