from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
# from django.template.loader import render_to_stringcreate_otp
from django.contrib.sites.shortcuts import get_current_site
from .models import EmailConfirmed
from django.shortcuts import get_object_or_404
from django.contrib import messages
from app_1.models import User



# sms sending
import http.client as ht
import json

import random


def login_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'boomboom_user/login_register.html')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = User.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
        
        
        
@csrf_exempt
def check_phone_exist(request):
    get_phon = request.POST.get("get_phon")
    user_obj = User.objects.filter(username=get_phon).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def create_otp(request):
    customer_phn_num = request.POST.get('id_sign_phone')
    
    #make random order ID
    otp_num = random.randint(11111, 99999)
    
    otp_num_str = str(otp_num)
    print(otp_num_str)
    
    
    customer_phn_numwith88 = "88"+customer_phn_num
    
    
    
    # sms sending
    conn = ht.HTTPSConnection("smsplus.sslwireless.com")
    headers = {'Content-type': 'application/json'}


    payload = {
     "api_token": "744d2817-6c3b-4a70-a91e-e3f9ee5cf1b",
     "sid": "BOOMBOOMNONAPI",
     "sms": otp_num_str + " is Your Signup OTP from boomboom",
     "msisdn": customer_phn_numwith88,
     "csms_id": "123456"
    }

    payload_json = json.dumps(payload)
    conn.request("POST", "/api/v3/send-sms", payload_json, headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    
    return HttpResponse(otp_num)
            
        

@csrf_exempt
def submit_signup_form(request):
    First_Name = request.POST.get("First_Name")
    Last_Name = request.POST.get("Last_Name")
    sign_email = request.POST.get("sign_email")
    sing_Password = request.POST.get("sing_Password")
    
    id_sign_phone =  request.POST.get("id_sign_phone")
    
    # otp 
    otp_numbr =  request.POST.get("otp_numbr")
    otp_cumtomer_input =  request.POST.get("otp_cumtomer_input")
    
    if otp_numbr == otp_cumtomer_input:
        print(First_Name, Last_Name, sign_email, sing_Password)
        
        # create user
        myuser = User.objects.create_user(id_sign_phone, sign_email, sing_Password)
        myuser.first_name = First_Name
        myuser.last_name = Last_Name
        myuser.is_active = True
        myuser.save()
        
        # logged in 
        user = authenticate(request, username=id_sign_phone, password=sing_Password)
        if user is not None:
            login(request, user)

        

        # # send mail
        # user = EmailConfirmed.objects.get(user=myuser)
        # site = get_current_site(request)
        # email = myuser.email
        # first_name = myuser.first_name
        # last_name = myuser.last_name
        # print('check1')

        # sub_of_email = "Activation Email From BoomBoom."

        # email_body = render_to_string(
        #     'boomboom_user/verify_email.html',{
        #         'first_name': first_name,
        #         'last_name': last_name,
        #         'email': email,
        #         'domain': site.domain,
        #         'activation_key': user.activation_key
        #     }
        # )


        # print('check2')
        # send_mail(
        #     sub_of_email,  # Subject of message
        #     email_body,  # Message
        #     '',  # From Email
        #     [email],  # To Email

        #     fail_silently=True
        # )

        return HttpResponse(True)
        
    else:
        return HttpResponse(False)



def email_confirm(request, activation_key):
    user= get_object_or_404(EmailConfirmed, activation_key=activation_key)
    if user is not None:
        user.email_confirmed=True
        user.save()

        myuser=User.objects.get(email=user)
        myuser.is_active=True
        myuser.save()
        first_name=myuser.first_name
        last_name=myuser.last_name

        condict = {'first_name': first_name, 'last_name':last_name}
        return render(request, 'boomboom_user/registration_complete.html', condict)



@csrf_exempt
def submit_login_form(request):
    login_email_or_num = request.POST.get("login_email")
    login_password = request.POST.get("login_password")
    
    
    # user = authenticate(request, username=login_email_or_num, password=login_password)
    # if user is not None:
    #     login(request, user)
    #     return HttpResponse(True)
    # else:
    #     ababa = User.objects.filter(email=login_email_or_num)
        
    #     return HttpResponse(False)
    
    if User.objects.filter(username=login_email_or_num):
        user = authenticate(request, username=login_email_or_num, password=login_password)
        if user is not None:
            login(request, user)
            return HttpResponse(True)
        else:
            return HttpResponse(False)
            
            
    elif User.objects.filter(email=login_email_or_num):        
        get_user = User.objects.get(email=login_email_or_num)
        get_us = get_user.username
        user = authenticate(request, username=get_us, password=login_password)
        if user is not None:
            login(request, user)
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    
        
    else:
        return HttpResponse(False)


def logout_func(request):
    # this is for logout from user id
    logout(request)
    return redirect('home')
