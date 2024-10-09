# Third-part library imports
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets

# Django imports
from django.conf import settings
import threading
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import  HttpRequest
from urllib.parse import unquote
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from collections import defaultdict

# Local modules imports
from members import serializers as members_serializers, models as members_models
from articles import serializers as articles_serializers, models as articles_models
from reservations import serializers as reservations_serializers, models as reservations_models
from users import serializers as users_serializers, models as users_models
from activities import models as activities_models, pagination as custom_pagination
from admins.models import Messages

import pickle
import os

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"


class ContactUs(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer
    
    def __init__(self, **kwargs: threading) -> None:
        super().__init__(**kwargs)
                
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        vectorizer_path = os.path.join(base_dir,'admins', 'vectorizer.pkl')
        model_path = os.path.join(base_dir, 'admins','spam_model.pkl')
        
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        with open(model_path, 'rb') as f:
            self.spam_model = pickle.load(f)

    def predict_spam(self, message):
        X = self.vectorizer.transform([message])
        return self.spam_model.predict(X)[0] == 1 # 1 refers to spam
    
    def send_email(self, subject, message, from_email, recipient_list, html_message):
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
    
    @action(detail=False, methods=['post'], permission_classes= [permissions.AllowAny, ])
    def send_message(self, request):
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            message_content = request.data.get('message', '')
            is_spam = self.predict_spam(message_content)
            ip_address = request.META.get("REMOTE_ADDR")
            
            if is_spam:
                serializer.save(is_spam = True, ip_address = ip_address)
                return Response({"detail": "Spam detected."}, status=status.HTTP_403_FORBIDDEN)
           
            else:
                serializer.save(is_spam = False, ip_address = ip_address)
                return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    def list_messages(self, request):
        paginator = custom_pagination.CustomPageNumberPaginator()

        messages = self.queryset.all()
        page = paginator.paginate_queryset(messages, request)
        
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)
    
    def message_details(self, request, pk):
        messages = self.queryset.get(pk = pk)
        serializer = self.serializer_class(messages)
        return Response(serializer.data)


    def admin_response(self, request, pk):
        message = self.get_object()
        sender_email = message.email
        reply = request.data.get('reply', '')
        email_context = {
            'reply': reply
        }
        email_html = render_to_string('email/contact_us.html', email_context)
        email_plain = strip_tags(email_html)
        
        threading.Thread(target=self.send_email, args=(
            'Welcome',
            email_plain,
            settings.EMAIL_HOST_USER,
            [sender_email],
            email_html
         )).start()        
        return Response({'message': 'Done'}, status=status.HTTP_200_OK)
    
# ---------------------------------- Statistics --------------------------------- #
from django.db.models.functions import TruncMonth

class Statistics(viewsets.ModelViewSet):
    
    def count_users(self, request):
        participant_users = users_models.User.objects.filter(user_type=users_models.User.UserType.PARTICIPANT).count()
        member_users = members_models.Member.objects.all().count()
        admin_users = users_models.User.objects.filter(user_type=users_models.User.UserType.ADMIN).count()
        total_users = participant_users + admin_users + member_users
        return Response({
            "total_users": total_users ,
        })
        
    def get_total_users(self, request):
        participant_users = users_models.User.objects.filter(user_type=users_models.User.UserType.PARTICIPANT).count()
        member_users = members_models.Member.objects.all().count()
        admin_users = users_models.User.objects.filter(user_type=users_models.User.UserType.ADMIN).count()

        return Response({
            "participants": participant_users,
            "members": member_users,
            "admins": admin_users
        })
        

    def get_new_users_over_time(self, request):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        new_users_over_time = users_models.User.objects.filter(created_at__date__gte=thirty_days_ago).extra(
            {"date": "date(created_at)"}
        ).values("date").annotate(count=Count("id"))

        return Response(new_users_over_time)      


    def count_activities(self, request):
        total_activities = activities_models.Activity.objects
        return Response({
            'total_activities': total_activities.count()
        })
        
    
    def total_activities(self, request):
        upcoming_activities = activities_models.Activity.objects.filter(start_at__gte=timezone.now())
        past_activities = activities_models.Activity.objects.filter(start_at__lt=timezone.now())
        hiking_activities = activities_models.Activity.objects.filter(activity_type = 4) 
        camping_activities = activities_models.Activity.objects.filter(activity_type = 1) 

        return Response({
            "past_activities": past_activities.count(),
            "upcoming_activities": upcoming_activities.count(),
            "hiking_activities": hiking_activities.count(),
            "camping_activities": camping_activities.count()
        })
   
    def past_activities(self, request):
        past_activities = activities_models.Activity.objects.filter(start_at__lt=timezone.now())
        location_counts = past_activities.values('location').annotate(count=Count('location'))
        response_data = {item['location']: item['count'] for item in location_counts}
        
        return Response(response_data)

    def past_activities_by_month(self, request, *args, **kwargs):
        # Filter activities that have ended before today
        past_activities = activities_models.Activity.objects.filter(start_at__lt=timezone.now())

        # Truncate the date to month and count by month
        month_counts = past_activities.annotate(month=TruncMonth('start_at')).values('month').annotate(count=Count('id'))

        # Format the response
        response_data = {item['month'].strftime('%b'): item['count'] for item in month_counts}

        return Response(response_data)

@api_view(['GET'])
def user_counts_by_location(request: HttpRequest):

    user_counts = defaultdict(int)
    
    for user in users_models.User.objects.all():
        user_counts[user.current_city] += 1

    return Response(user_counts)

    

# ---------------------------------- Filters --------------------------------- #

@api_view(['GET'])
def member_by_name(request: HttpRequest):
    try:

        member_name = request.query_params.get('member_name')

        if not member_name:
            return Response({
                'error': 'member_name is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        decoded_member_name = unquote(member_name)
        text_seq = decoded_member_name.split("_")

        members = members_models.Member.objects.filter(
            first_name__istartswith = text_seq[0]
        )

        if not members.exists():
            return Response({
                "error": "Member not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = members_serializers.ListMemberDataSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response("An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def article_by_name(request: HttpRequest):
    try:

        article_name = request.query_params.get('article_name')

        if not article_name:
            return Response({
                'error': 'article_name is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        decoded_article_name = unquote(article_name)
        text_seq = decoded_article_name.split("_")

        articles = articles_models.Article.objects.filter(
            article_name__istartswith = text_seq[0]
        )

        if not articles.exists():
            return Response({
                "error": "Article not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = articles_serializers.ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response("An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def user_by_name(request: HttpRequest):
    try:
        user_name = request.query_params.get('user_name')

        if not user_name:
            return Response({
                'error': 'user_name is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        decoded_user_name = unquote(user_name)
        text_seq = decoded_user_name.split("_")

        users = users_models.User.objects.filter(
            first_name__istartswith=text_seq[0]
        )

        if not users.exists():
            return Response({
                "error": "user not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = users_serializers.UserSerializer(users, many=True, context={'request': request})
        data = serializer.data
        
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response("An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def reservation_by_user_email(request: HttpRequest):
    try:

        user_email = request.query_params.get('user_email')

        if not user_email:
            return Response({
                'error': 'user_email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        decoded_user_email = unquote(user_email)
        text_seq = decoded_user_email.split("_")

        emails = reservations_models.AcceptedReservations.objects.filter(
            user__email__istartswith = text_seq[0]
        )

        if not emails.exists():
            return Response({
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = reservations_serializers.AcceptedReservationsSerializer(emails, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        print(e)
        return Response("An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
