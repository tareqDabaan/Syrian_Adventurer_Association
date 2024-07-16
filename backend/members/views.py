# Third-part library imports
from rest_framework.response import Response
from rest_framework import status,serializers, permissions, generics, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# Local modules imports
from members import serializers as memberserializer, models

# Django imports
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from collections import defaultdict
import pandas as pd        

#! ----------------------------------- Admin CRUD Members ---------------------------------- #

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing member data.

    - List all members: GET /members/
    - Retrieve a specific member: GET /members/<pk>/
    - Update a specific member: PATCH /members/<pk>/
    - Delete a specific member: DELETE /members/<pk>/

    Permissions:
        - List: Allowed for all users
        - Retrieve, Update, Delete: Admin users with appropriate permissions
    """

    queryset = models.Member.objects.all()
    serializer_class = memberserializer.ListMemberDataSerializer 

    def get_permissions(self):
        """
        Define permissions based on the action being performed.
        """
        if self.action in ['list']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.AllowAny]  # Require authentication
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.action in ['retrieve']:
            return memberserializer.RetrieveMemberDataSerializer
        return super().get_serializer_class()

    
    def list(self, request, *args, **kwargs):
        """
        List all members.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        response_data = []

        for item in data:
            item.pop('date_joined')
            item['date_joined'] = item.pop('date_joined_formatted')
            response_data.append(item)
            
        return Response(response_data, status=status.HTTP_200_OK)


    def retrieve(self, request, pk=None):
        """
        Retrieve a specific member.
        """
        queryset = self.get_queryset()
        try:
            member = queryset.get(pk=pk)
        except models.Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = memberserializer.ListMemberDataSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        """
        Update a specific member.
        """
        queryset = self.get_queryset()
        try:
            member = queryset.get(pk=pk)
        
        except models.Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(member, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """
        Delete a specific member.
        """
        queryset = self.get_queryset()
        try:
            member = queryset.get(pk=pk)
            member.delete()
        
        except models.Member.DoesNotExist:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'done':'member deleted successfully'},status=status.HTTP_204_NO_CONTENT)  # No content on successful deletion



class CreateMember(generics.GenericAPIView):
    """
    API endpoint for admins to create new members in the system.
    **Permissions:** Allowed for admins only.
    **HTTP Method:** POST
    **Response:**
        - On success (HTTP 200 OK):
            - "message": "Member successfully added"
            - "data": serialized member data

        - On validation error (HTTP 400 BAD REQUEST):
            - Detailed error messages from the serializer
    """
    serializer_class = memberserializer.ListMemberDataSerializer
    permission_classes = (permissions.IsAdminUser,) #todo change to Admins only
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()

            name = serializer.data['first_name']
            last_name = serializer.data['last_name']
            full_name = "{} {}".format(name, last_name)
            email = serializer.data['email']
            
            #? Send email to notify 
            subject = "Welcome to Adventurer, {}!".format(full_name)
            message = f"""
            Thank you for joining Adventurer, {full_name}!
            We're excited to have you on board and look forward to your engagement with the platform.
            If you have any questions or need assistance, please do not hesitate to reach out to our support team at [support email address].
            Sincerely,
            The Adventurer Team
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        
        except serializers.ValidationError as e:
            return Response(
                e.detail
                , status = status.HTTP_400_BAD_REQUEST
                )
        
        return Response({
            "message":"Member successfully added",
            "data": serializer.data},
            status = status.HTTP_200_OK
            )
        
        
class MembersID(APIView):
    
    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    def get(self, request, format = None):
        members = models.Member.objects.all(
            ).values('first_name'
                     , 'mid_name'
                     , 'last_name'
                     , 'id'
                     )
        
        response_data = [
            {
                'key': f"{member['first_name']} {member['mid_name']} {member['last_name']}",
                'value': member['id'],
            }
            
            for member in members
        ]
        response = Response(response_data, status = status.HTTP_200_OK)
        response['Access-Control-Allow-Origin'] = '*'
        return response                
    
#! ----------------------------------- End Admin CRUD Members ---------------------------------- #


# ------------------------------- Landing Page ------------------------------- #
class OurTeam(generics.ListAPIView): 
    """
    API endpoint to retrieve member data for the "Our Team" section on the landing page.
    **Permissions:** Allowed for all users (GET).
    **HTTP Method:** GET
    **Response:**
        A list of member data serialized using the `OurTeamSerializer`.

    """
    serializer_class = memberserializer.OurTeamSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return models.Member.objects.all()
  
from datetime import datetime

#* ------------------------ One Member in landing page ------------------------ #
class MemberActivityAPIView(APIView):
    """
    API endpoint to retrieve member data and associated activities for a specific member ID.
    **Permissions:** Allowed for all users (GET).
    **HTTP Method:** GET
    **Response:**
        - On success (HTTP 200 OK):
            - "member": serialized member data using `OneMemberSerializer`
            - "activities": serialized list of member's activities using `ActivitySerializer`

        - On member not found (HTTP 404 NOT FOUND):
            - "error": "Member does not exist"
    """
    def get(self, request, member_id):
    
        try:
            member = models.Member.objects.get(pk = member_id)
    
        except models.Member.DoesNotExist:
            return Response({"error": "Member does not exist"}, status = status.HTTP_404_NOT_FOUND)
        
        member_data = memberserializer.OneMemberSerializer(member).data
        activities_data = memberserializer.ActivitySerializer(member.activity_set.all(), many=True).data
        
        response_data = []
        
        for activity in activities_data:
            start_at_str = activity['start_at']
            start_at = datetime.strptime(start_at_str, '%Y-%m-%dT%H:%M:%S.%fZ')  # Adjust format as needed
            
            response_data.append(
                {
                    "activity_name": activity['activity_name'],
                    "image": activity['image'],
                    "start_at": start_at.strftime('%Y-%m-%d'),
                    "location": activity['location'],
                }
            )
        return Response({
            "member": member_data,
            "activities": response_data
            }, status = status.HTTP_200_OK)
        

@api_view(['GET'])
def analyze_member_ages(request):
    # Fetch members in Damascus
    damascus_members = models.Member.objects.filter(current_city='Damascus')

    # Convert QuerySet to pandas DataFrame
    df = pd.DataFrame(damascus_members.values('age'))  # Select only 'age' field

    # Calculate mean age
    mean_age = df['age'].mean()

    return Response({'mean_age': mean_age})  


@api_view(['GET'])
def get_member_counts_by_city(request):
    # Fetch members in Damascus
    member_counts = defaultdict(int)
    
    for member in models.Member.objects.all():
        member_counts[member.current_city] += 1

    # Return the dictionary as JSON response
    return Response(member_counts)


