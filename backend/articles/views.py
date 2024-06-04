# Third-part library imports
from rest_framework.response import Response
from rest_framework import status, permissions, generics

# Local modules imports
from .serializers import *
from .models import Article

# Django imports


class ArticlesAPI(generics.ListAPIView):
    """
    This API is used to List all articles
    
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    
class ArticleUploadAPI(generics.CreateAPIView):
    """
    This API is used to allow Admins to Upload a new article
    
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by = self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)
        


class AdminRUDArticles(generics.RetrieveUpdateDestroyAPIView):
    """
    This API is used to allow Admins to Retrieve, Update, Delete a specific article via it's ID
    """
    queryset = Article.objects
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save(uploaded_by = self.request.user)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        data = request.data.copy()
        data.pop('uploaded_by', None) #Remove the field from request data  
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        instance.delete()
        return Response({
            "details":"Deleted"
            },status = status.HTTP_204_NO_CONTENT)
    
from django.http import HttpResponse
import csv
def exportcsv(request):
    articles = Article.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=article.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'article_image', 'article_name', 'article_file', 'article_description', 'uploaded_by', 'uploaded_at'])
    art = articles.values_list('id', 'article_image', 'article_name', 'article_file', 'article_description', 'uploaded_by', 'uploaded_at')
    for std in art:
        writer.writerow(std)
    return response

