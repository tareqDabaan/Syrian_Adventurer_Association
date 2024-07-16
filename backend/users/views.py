# Third-part library imports
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets

# Local modules imports
from users import serializers as userserializer, models


#! ------------------- List User data in the Admin Dashboard ------------------ #
class ListParticipantsData(generics.ListAPIView):
    """
        This API will list the User's Data in the admin dashboard 
    """
    queryset = models.User.objects.filter(user_type = 'PARTICIPANT')
    serializer_class = userserializer.UserSerializer
    # permission_classes = (permissions.IsAdminUser, )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many = True)
        
        #? Customize the queryset to include necessary fields
        #todo ----------------------- Participated Activities ----------------------- #
        data = serializer.data
        
        #? Iterate through each item in the queryset and construct the 'full_name'
        
        return Response(data, status = status.HTTP_200_OK)

#! ------------------- End List User data in the Admin Dashboard ------------------ #
    
    
class ListData(viewsets.ReadOnlyModelViewSet):
    """
    An API to retrieve data related to users
    #TODO Not Done yet
    #!ALL DATA, with sensitive data (This might be used for user profile)
    #*It may retrieve a specific user data, or all users data   
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
    An API to retrieve user's data which will be used in the landing page #!accessable profile for everybody
    """
    serializer_class = userserializer.UserProfileSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = models.User.objects

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
