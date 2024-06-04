# Third-part library imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets

# Local modules imports
from reservations.models import Request, AcceptedReservations, RejectedReservations
from users.models import User
from reservations import serializers
import threading

# Django imports
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date
from django.core.mail import send_mail

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = serializers.RequestSerializer
    
    def send_email(self, subject, message, from_email, recipient_list, html_message):
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
     
    def list_pending_requests(self, request):
        pending_requests = self.queryset.filter(status='Pending')
        serializer = self.serializer_class(pending_requests, many=True)
        return Response(serializer.data)

    def approve_request(self, request, pk):
        reservation = self.get_object()
        reservation.status = 'Accepted'
        
        #? Extract Fields From Request
        activity = reservation.activity_id
        
        #? Create Reservation field
        AcceptedReservations.objects.create(user =  reservation.participant_id, activity_id = reservation.activity_id)
        
        #? Email context
        activity_date = activity.start_at.strftime('%Y-%m-%d')
        days_until_activity = (activity.start_at.date() - date.today()).days
        accept_image_url = 'https://imgs.search.brave.com/L71uQMhQgyrtRrrRBkHk4bzBE8A-3r-aSz3ODrjzXg4/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAyMS8x/MC8wOS8wMC8xNS9s/YW5kc2NhcGUtNjY5/MjcxMl82NDAuanBn'
        
        email_context = {
            'status': reservation.status,
            'activity_name': activity.activity_name,
            'activity_date': activity_date,
            'location': activity.location,
            'activity_description': activity.activity_description,
            'activity_fee': activity.activity_fee,
            'registration_deadline': activity.registration_deadline,
            'starting_point': activity.starting_point,
            'image_url': accept_image_url,
            'days_until_activity': days_until_activity
        }
        
        #? Render Email Template
        email_html = render_to_string('email/approval_notification.html', email_context)
        email_plain = strip_tags(email_html)
        
        #? Delete the request from table after accepting it
        reservation.delete()
        
        #? Send email notification asynchronously
        threading.Thread(target = self.send_email, args = (
            'Request Approved',
            email_plain,
            'admin@example.com',
            [reservation.participant_id.email],
            email_html
        )).start()
        
        return Response({'message': 'Request accepted'}, status=status.HTTP_200_OK)

        
    def reject_request(self, request, pk):
        reservation = self.get_object()
        reservation.status = 'Rejected'
        
        #? Extract Fields From Request
        reason = request.data.get('reason', '')
        activity = reservation.activity_id
        
        #? Create Reservation field
        RejectedReservations.objects.create(
            user = reservation.participant_id,
            activity_id = reservation.activity_id,
            reason = request.data.get('reason', '')
            )
        
        #? Email context
        activity_date = activity.start_at.strftime('%Y-%m-%d')
        days_until_activity = (activity.start_at.date() - date.today()).days
        reject_image_url = 'https://imgs.search.brave.com/-A-hBVUajDDQKzJIwZeGGcZjQIi-NRB7F7GIxOZV1rU/rs:fit:500:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvNDcx/MDg0NzE1L3Bob3Rv/L3J1YmJlci1zdGFt/cC1yZWplY3RlZC5q/cGc_cz02MTJ4NjEy/Jnc9MCZrPTIwJmM9/cXRRcmdIUWdGRm1I/LVRITm5JT0dYeEFE/UmFsZWEtaWVqTkx4/dEc3Sll6RT0'
        email_context = {
            'status': reservation.status,
            'activity_name': activity.activity_name,
            'activity_date': activity_date,
            'location': activity.location,
            'activity_description': activity.activity_description,
            'activity_fee': activity.activity_fee,
            'registration_deadline': activity.registration_deadline,
            'starting_point': activity.starting_point,
            'image_url': reject_image_url,
            'days_until_activity': days_until_activity,
            'reason': reason
        }
        
        #? Render Email Template
        email_html = render_to_string('email/approval_notification.html', email_context)
        email_plain = strip_tags(email_html)
    
        #? Delete the request from table after accepting it
        reservation.delete()
        
        #? Send email notification asynchronously
        threading.Thread(target=self.send_email, args=(
            'Request Rejected',
            email_plain,
            'admin@example.com',
            [reservation.participant_id.email],
            email_html
        )).start()
        
        return Response({'message': 'Request rejected'}, status=status.HTTP_200_OK)
    
     
class ActivityCountAPIView(APIView):
    def get(self, request, user_id):
        try:
            activity_count = Request.objects.filter(participant_id=user_id).count()
            return Response(
                {
                    'userID': user_id,
                    'participated activities': activity_count
                }
            )
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=404)
