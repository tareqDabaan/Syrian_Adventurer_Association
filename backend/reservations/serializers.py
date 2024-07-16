
from rest_framework import serializers
from .models import Request, AcceptedReservations, RejectedReservations
from users.models import User
from activities.models import Activity

class ActivityCountSerializer(serializers.Serializer):
    activities = serializers.IntegerField()
    
class AcceptedReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptedReservations
        fields = "__all__"
    def to_representation(self, instance: AcceptedReservations):
        # original_repr =  super().to_representation(instance)
      
        return {
            "user_email" : instance.user.email,
            "activity_name" : instance.activity_id.activity_name,
            "accepted_at" : instance.approved_at.strftime('%Y-%m-%d'),
        }    
        
        
        
class RejectedReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RejectedReservations
        fields = "__all__"
        
    def to_representation(self, instance: RejectedReservations):
        # original_repr =  super().to_representation(instance)
      
        return {
            "user_email" : instance.user.email,
            "activity_name" : instance.activity_id.activity_name,
            "rejected_at" : instance.rejected_at.strftime('%Y-%m-%d'),
            "reason": instance.reason
        }    
        
class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = "__all__"

    
    def to_representation(self, instance: Request):

        return {
            "request_id": instance.id,
            "user_email" : instance.participant_id.email,
            "activity_name" : instance.activity_id.activity_name,
            "activity_date" : instance.activity_id.start_at.date(),
            "request_date" : instance.request_created_at.date(),
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