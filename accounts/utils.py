import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify






def generateRandomToken():
    return str(uuid.uuid4())

def sendEmailToken(email, token):
    subject = "Verify Your Email Address"
    message = f"""Hi Please verify your email account by clicking this link 
    
    http://127.0.0.1:8000/accounts/verify-accounts/{token}

    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)
    


def sendOTPtoEmail(email, otp):
    subject = "OTP for Accont Login"
    message = f"""Hi, use this OTP to login
    
     <b>  {otp} </b>

    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)

def generateSlug(hotel_name):
    from .models import Hotel
    slug = slugify(hotel_name) + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generateSlug(hotel_name)
    return slug

