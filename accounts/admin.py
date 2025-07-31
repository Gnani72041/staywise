from django.contrib import admin
from .models import Ameneties, HotelUser, HotelVendor

class HotelUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'is_verified']
    

admin.site.register(HotelUser, HotelUserAdmin)
admin.site.register(HotelVendor, HotelUserAdmin)
admin.site.register(Ameneties)
