from django.contrib import admin
from activities import models

class ListD(admin.ModelAdmin):
    list_display = ('id','activity_name')



class Lista(admin.ModelAdmin):
    list_display = ('id','activity_type')
    
admin.site.register(models.Activity, ListD )
# admin.site.register(models.ActivityType)
admin.site.register(models.ActivityType, Lista)