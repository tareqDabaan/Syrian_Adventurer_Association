# Django imports
from django.core.mail import send_mail
from django.conf import settings
import random, string

# Local modules imports
from users.models import User 

import datetime
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
    
    subject = f'Welcome to Adventurer - Verify Your Account'
    otp = generate_otp()
    
    if hasattr(settings, 'OTP_EXPIRY_MINUTES'):
        # Use configured expiry time if available
        message = f"""
        Thank you for signing up with Adventurer!

        To complete your account setup, please enter the following one-time verification code:

        {otp}

        This code is valid for {settings.OTP_EXPIRY_MINUTES} minutes.

        Sincerely,

        The Adventurer Team
        """
    else:
        message = f"""
        Thank you for signing up with Adventurer!

        To complete your account setup, please enter the following one-time verification code:

        {otp}

        Please use this code promptly for security reasons.

        Sincerely,

        The Adventurer Team
        """
    
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.otp_sent_time = datetime.datetime.now()  # Add parentheses for function call
    user_obj.save()
