from django.contrib import admin
from activities import models

admin.site.register(models.Activity, )
admin.site.register(models.ActivityType)