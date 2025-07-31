from django.urls import path, re_path
from accounts import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),

    # ✅ Use regex to support email with special characters
    re_path(r'^send_otp/(?P<email>[^/]+)/$', views.send_otp, name='send_otp'),
    re_path(r'^verify_otp/(?P<email>[^/]+)/$', views.verify_otp, name='verify_otp'),

    path('login-vendor/',views.login_vendor, name='login_vendor'),
    path('register-vendor/', views.register_vendor, name='register_vendor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-hotel/', views.add_hotel, name='add_hotel'),
    path('<slug>/upload-images/',views.upload_images, name='upload_images'),
    path('delete-image/<id>/', views.delete_image, name='delete_image'),
    path('edit-hotel/<slug>/', views.edit_hotel, name='edit_hotel'),
    path('logout/', views.logout_view, name='logout_view'),

    path('verify-accounts/<token>/', views.verify_email_token, name='verify_email_token'),

]
