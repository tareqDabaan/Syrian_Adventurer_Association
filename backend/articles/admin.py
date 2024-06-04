from django.contrib import admin
from .import models

class Test(admin.ModelAdmin):
    list_display = ('article_name','uploaded_by','id',)

admin.site.register(models.Article, Test)