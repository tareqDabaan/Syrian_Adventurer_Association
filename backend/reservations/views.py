# Third-part library imports
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from rest_framework.decorators import action, permission_classes

# Local modules imports
from activities.pagination import CustomPageNumberPaginator
from reservations.models import Request, AcceptedReservations, RejectedReservations
from users.models import User
from reservations import serializers
from activities.models import Activity
# Django imports
import threading
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date
from django.core.mail import send_mail
from datetime import datetime


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = serializers.RequestSerializer
    pagination_class = CustomPageNumberPaginator
    def send_email(self, subject, message, from_email, recipient_list, html_message):
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
    @action(detail=False, methods=['post'], permission_classes= [permissions.IsAuthenticated, ])
    def create_request(self, request):
        #? Check user authenticity
        if not request.user.is_authenticated:
            return Response({
                "error": "activity_id is required"
                }, status=status.HTTP_400_BAD_REQUEST
            )
            
        data = request.data.copy()
        data['participant_id'] = request.user.id
      
        activity = data.get('activity_id')
        
        if not activity:
            return Response({
                "error": "activity_id is required"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            requested_activity = Activity.objects.get(pk = activity)
        except Activity.DoesNotExist:
            return Response({
                "error": "Activity not found"
                }, status=status.HTTP_404_NOT_FOUND)
         
        #? Check regestration date 
        if requested_activity.registration_deadline < datetime.now().date():
            return Response({
                "error": "Reservation deadline has passed"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        #? Check activity start date
        elif requested_activity.start_at.date() < datetime.now().date():
            return Response({
                "error": "Activity has started"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        current_participants = Request.objects.filter(activity_id = activity).count()
        
        #? Check max participants
        if current_participants >= requested_activity.max_participants:
            return Response({
                "error": "Maximum number of participants reached"
            }, status=status.HTTP_400_BAD_REQUEST) 
               
        serializer = serializers.CreateRequestSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
            
            if request.user.discount:
                discount_message = {
                    "discount":
                    f"activity fee was={requested_activity.activity_fee} and after discount={requested_activity.activity_fee * 80/100}"
                }
                return Response({
                    **serializer.data,
                    **discount_message
                    })
            else :
                return Response(
                    serializer.data,
                    status = status.HTTP_201_CREATED)
                
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST)
    
    def list_pending_requests(self, request):
        pending_requests = self.queryset.filter(status='Pending')
        page = self.paginate_queryset(pending_requests)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(pending_requests, many=True)
        return Response(serializer.data)
    
    def list_accepted_requests(self, request):
        accepted_requests = AcceptedReservations.objects.all()
        page = self.paginate_queryset(accepted_requests)
        if page is not None:
            serializer = self.get_paginated_response(serializers.AcceptedReservationsSerializer(page, many=True).data)
        else:
            serializer = serializers.AcceptedReservationsSerializer(accepted_requests, many=True)
        return Response(serializer.data)
    
    def list_rejected_requests(self, request):
        rejected_requests = RejectedReservations.objects.all()
        page = self.paginate_queryset(rejected_requests)
        if page is not None:
            serializer = self.get_paginated_response(serializers.RejectedReservationsSerializer(page, many=True).data)
        else:
            serializer = serializers.RejectedReservationsSerializer(rejected_requests, many=True)
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
            'image_url': accept_image_url,
            'days_until_activity': days_until_activity,
            'reservation_id': reservation.id  # Add this line

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
            'image_url': reject_image_url,
            'days_until_activity': days_until_activity,
            'reason': reason
        }
        
        #? Render Email Template
        email_html = render_to_string('email/rejected_notification.html', email_context)
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
    
     
class Statistics(viewsets.ModelViewSet):
    def get_activity_counts(self, request, user_id):
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


# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Activity
from django.contrib.gis.geos import Point


#Activity on map
@api_view(['GET'])
def get_activity_details(request):
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))
    point = Point(longitude, latitude, srid=4326)


    try:
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))

        # Create a Point object from the coordinates
        point = Point(longitude, latitude, srid=4326)

        # Iterate over all activities and check if any contains the point
        activities = Activity.objects.all()
        for activity in activities:
            if point in activity.point_on_map:
                return Response({
                    'activity_name': activity.activity_name,
                    # 'activity_images': [image.url for image in activity.images.all()]  # Assuming images are stored in another model related to Activity
                })

        return Response({'error': 'No activity found for this location'}, status=404)

    except ValueError:
        return Response({'error': 'Invalid latitude or longitude'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import AcceptedReservations

@csrf_exempt
def payment_page(request, reservation_id):
    reservation = get_object_or_404(AcceptedReservations, id=reservation_id)

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvc = request.POST.get('cvc')

        # Here you can add mock validation and processing logic
        if card_number and expiry_date and cvc:
            # Simulate successful payment
            return JsonResponse({'success': True})
        else:
            # Simulate payment failure
            return JsonResponse({'success': False}, status=400)

    return render(request, 'payment/mock_payment_form.html', {
        'reservation_id': reservation.id,
        'activity_fee': reservation.activity_id.activity_fee
    })


def process_mock_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvc = request.POST.get('cvc')

        # Here you can add mock validation and processing logic
        if card_number and expiry_date and cvc:
            # Simulate successful payment
            return redirect('payment_success')
        else:
            # Simulate payment failure
            return redirect('payment_failure')
    return redirect('home')
