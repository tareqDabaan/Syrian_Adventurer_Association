# Django imports
from django.urls import path

# Local modules imports
from articles import views

app_name = "articles"

urlpatterns = [

    
    # --------------------------------- Endpoints -------------------------------- #
    #! Admin Dashboard
    
    path('upload_article/', views.ArticleUploadAPI.as_view()),
    path('rud_article/<int:pk>', views.AdminRUDArticles.as_view()),
    # path('exportcsv/', views.exportcsv),
    
    #! Article page
    path('list_articles/', views.ArticlesAPI.as_view()),
    # --------------------------------- End Endpoints -------------------------------- #
    
]
