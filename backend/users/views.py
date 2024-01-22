# Third-part library imports
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed

# Local modules imports
from users import serializers as userserializer, models


class Listdaa(viewsets.ReadOnlyModelViewSet):
    """
    
    """
    serializer_class = userserializer.UserSerializer
    queryset = models.User.objects
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]
    

class UserProfile(generics.ListAPIView):
    """
    
    """
    serializer_class = userserializer.UserProfileSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = models.User.objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class ListMemberData(generics.ListAPIView):
    """
    This API is used to list the member's data 
    Permissions: Allowed for all
    """
    serializer_class = userserializer.ListMemberDataSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = models.Member.objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
