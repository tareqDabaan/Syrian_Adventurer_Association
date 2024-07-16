from django.contrib import admin
from .models import Preferences
from .utils import generate_csv_response


@admin.action(description='Export preferences as CSV')
def export_as_csv(modeladmin, request, queryset):
    return generate_csv_response(queryset)

class PreferencesAdmin(admin.ModelAdmin):
    actions = [export_as_csv]

admin.site.register(Preferences,PreferencesAdmin)