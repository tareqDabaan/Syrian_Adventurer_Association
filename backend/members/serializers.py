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
    
    
    #! Activity, Member Images
    class Meta:
        model = Member
        fields = ['id','profile_image','first_name', 'last_name', 'age', 'date_joined']
        
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)  # Extract and remove 'fields' argument
        super().__init__(*args, **kwargs)
        if fields:
            self.Meta.fields = fields
            
    def get_profile_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.profile_image.url)
        return obj.profile_image.url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        full_name = "{} {}".format(instance.first_name, instance.last_name)
        started_at = instance.date_joined.date()
        representation['id'] = instance.id
        representation['full_name'] = full_name
        representation['started_at'] = started_at
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activity_name', 'image', 'start_at', 'location']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.image:
            representation['image'] = request.build_absolute_uri(instance.image.url)
        
        return representation
    
class OneMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'profile_image', 'last_name', 'age', 'date_joined', 'current_city', 'social_media_profiles']

    def to_representation(self, instance):
        full_name = "{} {}".format(instance.first_name, instance.last_name)
        request = self.context.get('request')
        image_url = None
        started_at = instance.date_joined.date()

        if instance.profile_image:
            image_url = request.build_absolute_uri(instance.profile_image.url)

        return {
            "id": instance.id,
            "full_name": full_name,
            "profile_image": image_url,
            "started_at": started_at,
            "age": instance.age,
            "location": instance.current_city,
            "social_media_accounts": instance.social_media_profiles,
        }