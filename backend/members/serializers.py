# Third-part library imports
from rest_framework import serializers

# Local modules imports
from members.models import *
from activities.models import Activity

class RetrieveMemberDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'age', 'date_joined', 'current_city', 'social_media_profiles']

    def to_representation(self, instance):
        full_name = "{} {}".format(instance.first_name, instance.last_name)

        return {
            "id": instance.id
            , "full_name": full_name
            , "current_city":instance.current_city
            , "started_at": instance.date_joined
            , "age": instance.age
            , "social_media_accounts": instance.social_media_profiles
        }
    

class ListMemberDataSerializer(serializers.ModelSerializer):
    date_joined_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = '__all__'  

    def get_date_joined_formatted(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')


class OurTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Member
        fields = ['profile_image','first_name', 'last_name', 'age', 'date_joined']

    def to_representation(self, instance):
        full_name = "{} {}".format(instance.first_name, instance.last_name)
        
        image_url = None
        started_at = instance.date_joined.date()
        
        if instance.profile_image:
            image_url = instance.profile_image.url
            
        return {
            "id": instance.id
            , "full_name": full_name
            , "started_at": started_at
            , "age": instance.age
            , "image": image_url
        }

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity_name', 'image']
      
class OneMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'profile_image', 'last_name', 'age', 'date_joined', 'current_city', 'social_media_profiles']
        
    def to_representation(self, instance):
        full_name = "{} {}".format(instance.first_name, instance.last_name)
        
        image_url = None
        started_at = instance.date_joined.date()
        
        if instance.profile_image:
            image_url = instance.profile_image.url
            
        return {
            "id": instance.id
            , "full_name": full_name
            , "profile_image": image_url
            , "started_at": started_at
            , "age": instance.age
            , "location": instance.current_city
            , "social_media_accounts": instance.social_media_profiles
        }