# Django imports
from django.core.mail import send_mail
from django.conf import settings
import random, string

# Local modules imports
from users.models import User 


#? Function to generate random 6-digit code  
def generate_otp():
    """Generates a random 6-digit OTP."""
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(6))


#? Function to send verification code to users
def send_otp_via_email(email):
    """
    This function is used to send the OTP code to the email 
    """
    subject = f'Welcome to Adventurer, verify your account '
    otp = generate_otp()
    message = f'Your verification code is: {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()
