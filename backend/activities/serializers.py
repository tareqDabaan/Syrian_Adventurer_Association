from activities.models import Activity, ActivityType
from rest_framework import serializers
from members.models import Member
        
class MemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['name', 'profile_image']  

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    
class ActivityDetailsSerializer(serializers.ModelSerializer):
    members =  serializers.SerializerMethodField()
  
    class Meta:
        model = Activity
        fields = ['id','activity_name','activity_description', 'point_on_map',
                  'image', 'members']
    
    def get_members(self, obj):
        members_data = MemberSerializer(obj.members, many = True).data
        for member in members_data:
            return {
                'name': member['name'],
                'profile_image': member['profile_image']
            }


class ActivitySerializer(serializers.ModelSerializer):
    members =  MemberSerializer(many = True, read_only = True)
    
    class Meta:
        model = Activity
        fields = ['activity_name','activity_description', 'point_on_map',
                'image', 'members']


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

            
class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'   
            
            


            
            
            
    #!Solve Image ###################
class UpComingActivitySerializerLimited(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'       
    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url    
    
    def to_representation(self, instance: Activity):
        representation = super().to_representation(instance)
        representation["id"]= instance.id,
        representation["name"]= instance.activity_name,
        representation["start_at"]= instance.start_at.date(),
        representation["ends_at"]= instance.ends_at,
        representation["activity_type"]= instance.activity_type.activity_type,
        representation["location"]= instance.location,
        return representation
class ActivityFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'       
        
    def to_representation(self, instance: Activity):
        image_url = None
        if instance.image:
            image_url = instance.image.url
        
        return {
            "id": instance.id,
            "image": image_url,
            "activity_name": instance.activity_name,
            "start_at": instance.start_at.date(),
            "ends_at": instance.ends_at,
            "activity_type": instance.activity_type.activity_type,
            "location": instance.location,
        }
# ----------------------------------- ADMIN ---------------------------------- #

class RUDActivitySerializer(serializers.ModelSerializer):
    
    
    #! Actuvuty type sd
    activity_type = ActivityTypeSerializer()
    members =  MemberSerializer(many = True, read_only = True)
    class Meta:
        model = Activity
        fields = '__all__'
        
          
class CreateActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'
        