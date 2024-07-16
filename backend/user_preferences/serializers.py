from rest_framework import serializers
from .models import Preferences

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = '__all__'