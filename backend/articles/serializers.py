from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.email')
    
    class Meta:
        model = Article
        fields = '__all__'
        
    def to_representation(self, instance):
        full_name = "{} {} {}".format(instance.uploaded_by.first_name, instance.uploaded_by.mid_name, instance.uploaded_by.last_name)
        data = super().to_representation(instance)
        data['uploaded_by'] = full_name

        return data
    