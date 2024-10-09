# Third-part library imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets

# Local modules imports
from gallery.serializers import *
from gallery.models import Gallery

# Django imports
from django.http import Http404


class GalleryUploadAPI(generics.CreateAPIView):
    """
    This API is used to allow Admins to Upload a new picture to the gallery
    
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    # permission_classes = (permissions.IsAdminUser,)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by = self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)
    
    
####COMPLETE DELETE
class GalleryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing gallery data.

    - List all pictures
    - Retrieve a specific picture
    - Delete a specific picture

    Permissions:
        - List: Allowed for all users
        - Retrieve, Update, Delete: Admin users with appropriate permissions
    """

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer 

    def get_permissions(self):
        """
        Define permissions based on the action being performed.
        """
        if self.action in ['list']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]  # Require authentication
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.action in ['retrieve']:
            return self.serializer_class ####    
        return super().get_serializer_class()


    def list(self, request, *args, **kwargs):
        """
        List all pictures.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """
        Retrieve a specific picture.
        """
        queryset = self.get_queryset()
        try:
            gallery = queryset.get(pk=pk)
        except Gallery.DoesNotExist:
            return Response({'error': 'Picture not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(gallery)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GalleryDeleteView(APIView):
    """
    This API is used to allow Admins to delete a specific picture
    """

    def get_object(self, pk):
        try:
            return Gallery.objects.get(pk=pk)
        except Gallery.DoesNotExist:
            raise Http404

    def has_permissions(self, request):
        return request.user and request.user.is_staff

    def delete(self, request, pk, format=None):
        if not self.has_permissions(request):
            return Response({
                "detail": "Authentication credentials were not provided."
                }, status=status.HTTP_401_UNAUTHORIZED)

        gallery = self.get_object(pk)
        gallery.delete()
    
        return Response({
            "deleted": f"Gallery picture with id={pk} has been deleted"
            }, status=status.HTTP_204_NO_CONTENT)
