from django.contrib import admin
from users import models as usermodels 

class Test(admin.ModelAdmin):
    list_display = ('email','user_type',)
admin.site.register(usermodels.User, Test)
admin.site.register(usermodels.PasswordReset)