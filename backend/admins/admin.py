from django.contrib import admin
from admins import models



class ListDisplay(admin.ModelAdmin):
    list_display = ('id','sender_name', 'email')
    
    def sender_name(self, obj):
        return obj.name
    sender_name.short_description = 'SenderName'
admin.site.register(models.Messages, ListDisplay)