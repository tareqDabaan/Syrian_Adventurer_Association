
from rest_framework import serializers
from .models import Request
from users.models import User
from activities.models import Activity

class ActivityCountSerializer(serializers.Serializer):
    activities = serializers.IntegerField()


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

    
    def to_representation(self, instance: Request):
        # original_repr =  super().to_representation(instance)
        # original_repr["user_email"] = instance.participant_id.email
        # original_repr["location_id"] = instance.service.provider_location.id
        # original_repr["provider_id"] = instance.service.provider_location.service_provider.id
        # original_repr["provider_email"] = instance.service.provider_location.service_provider.email
        # original_repr["provider_business_name"] = instance.service.provider_location.service_provider.business_name
        
        return {
            "request_id": instance.id,
            "user_email" : instance.participant_id.email,
            "activity_name" : instance.activity_id.activity_name,
            "activity_date" : instance.activity_id.start_at,
            "request_date" : instance.request_created_at,
            "request_status" : instance.status,
        }

    # {
    #     "id": 6,
    #     "reservation_created_at": "2024-06-02T20:13:54.477071Z",
    #     "status": "('Pending', 'Pending')",
    #     "participant_id": 6,
    #     "activity_id": 21,
    #     "user_email": "test2@gmail.com",
    #     "activity_name": "Activity three",
    #     "activity_date": "2024-06-21T19:57:00Z",
    #     "reservation_status": "('Pending', 'Pending')"
    # },