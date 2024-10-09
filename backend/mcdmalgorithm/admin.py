from django.contrib import admin
from .models import Dataset
import csv
from django.http import HttpResponse

import random

from rest_framework.decorators import api_view

from rest_framework.response import Response

    
def generate_csv_response(preferences_queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_preferences.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Budget', 'Preferred Month',
        'Preferred Places', 'Preferred Types', 'Preferred Difficulty', 'More Than a Day'
    ])

    for pref in preferences_queryset:
        writer.writerow([
            pref.id, pref.budget, pref.preferred_month,
            pref.preferred_places, pref.preferred_types, pref.preferred_difficulity, pref.more_than_day
        ])

    return response

@admin.action(description='Export preferences as CSV')
def export_as_csv(modeladmin, request, queryset):
    return generate_csv_response(queryset)

class PreferencesAdmin(admin.ModelAdmin):
    actions = [export_as_csv]
admin.site.register(Dataset, PreferencesAdmin)
