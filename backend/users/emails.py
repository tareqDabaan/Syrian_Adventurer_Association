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

from django.template.loader import render_to_string

#? Function to send verification code to users
def send_otp_via_email(email):
    """
    Sends the OTP code to the user's email using an HTML template.
    """

    subject = 'Welcome to Adventurer - Verify Your Account'
    otp = generate_otp()

    # Render the HTML template with OTP
    html_message = render_to_string('email/signup.html', {'otp': otp})

    # Send the email
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, '', email_from, [email], html_message=html_message)

    # Update user's OTP and OTP sent time
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.otp_sent_time = datetime.datetime.now()
    user_obj.save()
