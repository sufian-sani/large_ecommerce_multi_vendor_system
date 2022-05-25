from django.urls import path
from . import views


urlpatterns=[
    path('',views.login_register,name='login_register'),
    path('check_email_exist',views.check_email_exist,name='check_email_exist'),
    path('check_phone_exist', views.check_phone_exist, name='check_phone_exist'),
    path('create_otp', views.create_otp, name='create_otp'),
    
    path('submit_signup_form',views.submit_signup_form,name='submit_signup_form'),
    path('submit_login_form',views.submit_login_form,name='submit_login_form'),
    path('logout_func',views.logout_func,name='logout_func'),

    # activation email
    path('email/confirmation/<str:activation_key>/', views.email_confirm, name='email_activation'  ),

]

