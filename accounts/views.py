from django.shortcuts import render,redirect
from .models import HotelUser, HotelVendor, Hotel, Ameneties, HotelImages
from django.db.models import Q
from django.contrib import messages
from .utils import generateRandomToken, sendEmailToken, sendOTPtoEmail
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
import random
from django.contrib.auth.decorators import login_required
from .utils import generateSlug
from django.http import HttpResponseRedirect


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        hotel_user = HotelUser.objects.filter(
            email=email) 

        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified.")
            return redirect('/accounts/login/')


        hotel_user = authenticate(username = hotel_user[0].username, password = password)
        if hotel_user:
            messages.success(request, "Login Successful.")
            login(request, hotel_user)
            return redirect('/accounts/login/')
        
        messages.warning(request, "Invalid Credentials")
        return redirect('/accounts/login/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register/')
        

        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            email_token=generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()
        sendEmailToken(email, hotel_user.email_token)

        messages.success(request, "Email sent to your Email.")
        return redirect('/accounts/register/')

    return render(request, 'register.html')

def verify_email_token(request, token):
    try:
        
        hotel_user = HotelUser.objects.get(email_token=token)
        hotel_user.is_verified = True
        hotel_user.save()
        messages.success(request, "Email Verified Successfully.")
        return redirect('/accounts/login/')
    except Exception as e:
        return HttpResponse("Invalid Token")
    


def send_otp(request, email):
    hotel_user = HotelUser.objects.filter(
            email=email) 
    if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login/')
    otp = random.randint(1000, 9999)
    hotel_user.update(otp = otp)
    
    
    sendOTPtoEmail(email, otp)

    return redirect(f'/accounts/verify_otp/{email}/')


def verify_otp(request, email):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        hotel_user= HotelUser.objects.get(email=email)

        if otp == hotel_user.otp:
            messages.success(request, "Login Successful.")
            login(request, hotel_user)
            return redirect('/accounts/login/')
        messages.warning(request, "Wrong OTP")    
        return redirect(f'/accounts/verify_otp/{email}/')
    
    return render(request, 'verify_otp.html')










def login_vendor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        hotel_user = HotelVendor.objects.filter(
            email=email) 

        if not hotel_user.exists():
            messages.warning(request, "No Account Found.")
            return redirect('/accounts/login-vendor/')

        if not hotel_user[0].is_verified:
            messages.warning(request, "Account not verified.")
            return redirect('/accounts/login-vendor/')


        hotel_user = authenticate(username = hotel_user[0].username, password = password)
        if hotel_user:
            messages.success(request, "Login Successful.")
            login(request, hotel_user)
            return redirect('/accounts/dashboard/')
        
        messages.warning(request, "Invalid Credentials")
        return redirect('/accounts/login-vendor/')

    return render(request, 'vendor/login_vendor.html')


def register_vendor(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email=email) | Q(phone_number=phone_number)
        )

        if hotel_user.exists():
            messages.warning(request, "Account exists with Email or Phone Number.")
            return redirect('/accounts/register-vendor/')
        

        hotel_user = HotelVendor.objects.create(
            username = phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            business_name=business_name,
            email_token=generateRandomToken(),
        )
        hotel_user.set_password(password)
        hotel_user.save()
        sendEmailToken(email, hotel_user.email_token)

        messages.success(request, "Email sent to your Email.")
        return redirect('/accounts/register-vendor/')

    return render(request, 'vendor/register_vendor.html')


@login_required(login_url='login_vendor')
def dashboard(request):
    context = {'hotels' : Hotel.objects.filter(hotel_owner=request.user)}
    return render(request,'vendor/vendor_dashboard.html',context)

@login_required(login_url='login_vendor')
def add_hotel(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        ameneties = request.POST.getlist('ameneties')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_slug = generateSlug(hotel_name)
        
        hotel_vendor = HotelVendor.objects.get(id = request.user.id)



        hotel_obj = Hotel.objects.create(
            hotel_name = hotel_name,
            hotel_description = hotel_description,
            hotel_price = hotel_price,
            hotel_offer_price = hotel_offer_price,
            hotel_location = hotel_location,
            hotel_slug = hotel_slug,
            hotel_owner = hotel_vendor,

        )

        for amenity in ameneties:
            amenity_obj = Ameneties.objects.get(id=amenity)
            hotel_obj.ameneties.add(amenity_obj)
            hotel_obj.save()

        messages.success(request, "Hotel Added Successfully.")
        return redirect('/accounts/add-hotel/')
    
    ameneties = Ameneties.objects.all()


    return render(request,'vendor/add_hotel.html',context={
        'ameneties': ameneties})




@login_required(login_url='login_vendor')
def upload_images(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.method == "POST":
        image = request.FILES.get('image')
        print(image)
        HotelImages.objects.create(
            hotel = hotel_obj ,
            image = image
        )
        return HttpResponseRedirect(request.path_info)
        
    return render(request,'vendor/upload_images.html',context={'images': hotel_obj.hotel_images.all()})




@login_required(login_url='login_vendor')
def delete_image(request, id):
    print("#########")
    print(id)
    print("#########")
    hotel_image = HotelImages.objects.get(id = id)
    hotel_image.delete()
    messages.success(request, "Image Deleted Successfully.")
    return redirect('/accounts/dashboard/')  # Use URL name, not raw path

        
  
@login_required(login_url='login_vendor')
def edit_hotel(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug=slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not allowed to edit this hotel.")
    
    if request.method == "POST":
        hotel_name = request.POST.get('hotel_name')
        hotel_description = request.POST.get('hotel_description')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('hotel_location')
        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()
        messages.success(request, "Hotel Details Updated Successfully.")


        return HttpResponseRedirect(request.path_info)
    ameneties = Ameneties.objects.all()
    return render(request,'vendor/edit_hotel.html',context={'hotel': hotel_obj,'ameneties': ameneties})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('/accounts/login/')  

