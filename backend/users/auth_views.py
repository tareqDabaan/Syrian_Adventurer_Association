# Third-part library imports
from typing import Any
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets, mixins
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Local modules imports
from users import serializers as userserializer, emails, models
from .serializers import MyTokenObtainPairSerializer

# Django imports
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
import datetime
import threading

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class Signup(APIView):
    """
    This API is used to signup (register a new user)
    Provide email, password and confirm password and then verify your account via the code sent to the email 
    Permissions: Allowed for all
    """

    permission_classes = (permissions.AllowAny, )
    serializer_classes = userserializer.SignupSerializer

    def post(self, request):

        try:
            data = request.data
            serializer = self.serializer_classes(data = data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
        
            email_thread = threading.Thread(target = emails.send_otp_via_email, args = (serializer.data['email'], ))
            email_thread.start()
        except serializers.ValidationError as e:
            return Response(e.detail, status = status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message":"Successfully done, please check your email to verify your account"
            }, status = status.HTTP_200_OK)

# ---------------------------------------------------------------------------- #
#!Not completed ... Check time expiry 
class VerifyAccount(APIView):
    """
    This API is used to verify user's account 
    Provide email and OTPCode to verify the account and then login using the account
    Permissions: Allowed for all
    """
    serializer_classes = userserializer.VerifyAccountSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_classes(data = data)
            
            if serializer.is_valid(raise_exception=True):
                #? Get the entered email and OTP code to verify validation
                email = serializer.data['email']
                otp = serializer.data['otp']
    
                user = models.User.objects.filter(email = email)
                
                #? Check if the entered email is valid 
                if not user.exists():
                    return Response({
                        "error":"Invalid email"
                        }, status = status.HTTP_400_BAD_REQUEST)
              
                user = user.first()

                #? Check if the entered OTP code matches the sent code 
                if user.otp != otp:
                   
                    return Response({
                        "error":"Wrong verification code"
                        }, status = status.HTTP_400_BAD_REQUEST) 
                
                user.is_verified = True #? Update user's account status and save it
                user.otp = None #? Delete the otp after verification
                user.save()

        #? Check for validation errors (otp length > 6, otp is not digit)
        except serializers.ValidationError as validation_error: 
            return Response(validation_error.detail
                            , status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            
            return Response({
                "error": "Internal server error"
                }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        return Response({
                "message":"Account verified, you can login now"
                }, status = status.HTTP_200_OK)

# ---------------------------------------------------------------------------- #

class ReGenerateOTPCode(APIView):
    """
    This API is used to Regenerate OTP code  
    Provide an access & authenticated email and you'll get the OTP code
    """
    def post(self, request):
        #? Get the user email
        email = request.data.get('email', '')
    
        #? Check if their is a user with the submitted email
        if not email:
            return Response({
                "error":"Email field is required"
            }, status = status.HTTP_400_BAD_REQUEST)
        
        #? Retrieve the user from the database
        try:
            user = models.User.objects.get(email=email)
        
        except models.User.DoesNotExist:
            return Response({
                'error': 'User with this email does not exist.'
                }, status = status.HTTP_404_NOT_FOUND)

        #? Resend the code to the email
        otp = emails.generate_otp()
        user.otp = otp
        user.save()
        emails.send_otp_via_email(email)

        return Response({
            'message': 'Verification code has been sent to your email.'
            }, status = status.HTTP_200_OK)
        
# ---------------------------------------------------------------------------- #

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password') 
    
        user = authenticate(email = email, password = password)
        if user is None:
            return Response({'error':'invalid'})
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        response = Response({'access':str(access_token)})
        response.set_cookie(key = 'refresh', value = str(refresh), httponly = True)
        
        return response
# ---------------------------------------------------------------------------- #

class ExRefresh(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'error':'Refresh token not found'}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
        except Exception as e:
            return Response({'error':str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
        response = Response({'access':str(access_token)})
        response.set_cookie(key = 'refresh', value = str(refresh), httponly = True)
        print(f"refresh printed:{refresh}")
        return response
# ---------------------------------------------------------------------------- #
class LogoutAPI(generics.GenericAPIView):
    serializer_class = userserializer.LogoutSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response({
            "message":"Logged out successfully "
            }, status = status.HTTP_200_OK)


class LogoutTest(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key = 'refresh')
        response.data = {
            'message': 'Logged out successfully'
        }
        return response
# ---------------------------------------------------------------------------- #

class ChangePassword(generics.UpdateAPIView):
    """
    This API is used to allow users change their password when they need
    Provide old_password and new_password and the password will be updated
    Permissions: Allowed for authenticated users only  
    """
    serializer_class = userserializer.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset = None):
        obj = self.request.user
        return obj
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            
            #? Check if the entered password is correct
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({
                    "old_password":"Wrong password"
                }, status = status.HTTP_400_BAD_REQUEST)
        
            #? Update the user password and set the new password
            self.object.set_password(serializer.data.get('new_password')) 
            self.object.save()
        
            return Response({
                "message":"Password updated successfully"
            }, status = status.HTTP_200_OK)
        
        return Response(
            serializer.errors
            , status = status.HTTP_400_BAD_REQUEST
            )
    
# ---------------------------------------------------------------------------- #

class RequestPasswordReset(generics.GenericAPIView):
    """
    This API is used to allow users send a request to reset their password if they forgot it
    It's the first step for password reset, User provides his email and then he will get a 6-digits code to reset the password
    Provide the email 
    Permissions: Allowed for all
    """
    serializer_class = userserializer.PasswordResetRequestSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        user = models.User.objects.filter(email = serializer.validated_data['email']).first()

        #? Check if user requested exists and verified
        if user:
            if user.is_verified:
                otp = emails.generate_otp()
                models.PasswordReset.objects.create(user = user, otp = otp)
                
                #? Send email code
                def send_email_async():
                    # Load HTML template
                    html_content = render_to_string('email/password_reset_code.html', {'otp': otp, 'user': user})

                    # Send email using EmailMultiAlternatives for HTML only
                    msg = EmailMultiAlternatives(
                        'Password Reset Code',
                        html_content,
                        'your_email@example.com',  # Replace with your sender email
                        [user.email]
                    )
                    msg.content_subtype = 'html'  # Ensure content type is set to HTML
                    msg.send()

                # Create and start a new thread for sending email
                email_thread = threading.Thread(target=send_email_async)
                email_thread.start()
                
                return Response({
                    'success': f'Password reset code sent to {user}'
                    }, status = status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'User is not verified'
                    }, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'No user found for this email'
                }, status = status.HTTP_404_NOT_FOUND)

# ---------------------------------------------------------------------------- #

class PasswordResetVerifyCode(generics.GenericAPIView):
    """
    This API is used to verify the reset password code that the user provides to reset the password 
    It's the second step for password reset, User provides the code to be checked 
    Provide the code 
    Permissions: Allowed for all
    """
    serializer_class = userserializer.OTPcheck
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)

        otp = serializer.validated_data['otp']
        password_reset = models.PasswordReset.objects.filter(otp = otp).first()

        #? Check if object exists and otp is correct
        if password_reset:
            user = password_reset.user
            password_reset.can_update_password = True
            password_reset.save()
            
            return Response({
                "message": "Succeed, you can set a new password now"
                }, status=status.HTTP_200_OK)

        else:
            return Response({
                "error": "Invalid or expired code"
                }, status=status.HTTP_400_BAD_REQUEST)
        
# ---------------------------------------------------------------------------- #

class PasswordReset(generics.UpdateAPIView):
    """
    This API is used to verify the allow users to reset their password after verification 
    It's the last step for password reset, User password will be reset
    Provide the email, new password, re password 
    Permissions: Allowed for all
    """
    serializer_class = userserializer.OTPVerificationSerializer
    permission_classes = (permissions.AllowAny,)  

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        email = serializer.validated_data['email']
        user = models.User.objects.filter(email = email).first()
        password_reset = get_object_or_404(models.PasswordReset, user = user)

        new_password = serializer.validated_data['new_password']
        re_password = serializer.validated_data['re_password']
        
        #? Check for the request
        if not password_reset:
           return Response({
               "error": "Password reset request has expired"
               }, status=status.HTTP_400_BAD_REQUEST)

        #? Check if user verified the email, he can update his password
        if password_reset.can_update_password:

            #? Check that password fields match
            if new_password == re_password:
                user.set_password(new_password)
                user.save()
                password_reset.delete()
                
                return Response({
                    "success": "Password has been reset"
                    }, status=status.HTTP_200_OK)
            
            else:
                return Response({
                    "password_error": 'Password fields does not match'
                    }, status = status.HTTP_400_BAD_REQUEST)
       
        else:
            return Response({
                "error": "Please verify you're email to reset your password"
                }, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------------- #

class CompleteSignUp(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
    This API is used to allow users to complete their profile 
    User Provide the required data to complete his profile  
    Permissions: Allowed for authenticated users only
    """

    serializer_class = userserializer.CompleteSignUpSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.User.objects.all()

    today = datetime.datetime.now().date()
    year = today.year

    def __init__(self, **kwargs: Any) -> None:
        print(self.year)
        super().__init__(**kwargs)

    def get_object(self):
        return self.request.user
    