from django.shortcuts import render,redirect
from django.contrib import messages
import random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import requests
import re
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from accounts.models import UserAuth
from email.utils import formataddr
from django.db.models import Q
from django.core.validators import validate_email
from datetime import datetime
from django.contrib.auth.decorators import login_required








def login(request):
    if request.method == "GET":
        try:
            user_id = UserAuth.objects.get(user_id=request.user.user_id)
            return redirect("dashboard")
        except:
            return render(request,'user_auth/login.html')
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        email = email.lower()

        user = authenticate(email=email,password = password)
        if not user:
            messages.warning(request, 'invalid login details')
            return redirect('login')
        
        else:
            auth_login(request,user)
    return redirect("dashboard")

def signup(request,sponsor_id=''):
    if request.method == "GET":
        data = {
            'sponsor_id':sponsor_id
        }
        return render(request,'user_auth/signup.html',context=data)

    if request.method =="POST":
        username = str(request.POST.get('username', '')).strip().lower()
        email = str(request.POST.get('email')).lower().strip()
        referrar_id = request.POST.get('referrar_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6LenG9cqAAAAAN-KkXViE0MVd1hrBKXTz_jTD8nI'
        captchaData = {'secret':secretkey,'response':clientkey}
        r= requests.post('https://www.google.com/recaptcha/api/siteverify',data = captchaData)
        response = json.loads(r.text)
        verify = response['success']
        user_input_data ={
            'username':username,
            'email':email,
            'referrar_id':referrar_id,
        }
        if "@gmail.com" not in email:
            messages.info(request, "Please enter a valid Gmail address.")
            return render(request, 'user_auth/signup.html', user_input_data)
        try:
            validate_email(email)
        except:
            messages.info(request, "Invalid Email Address.")
            return render(request, 'user_auth/signup.html', user_input_data)
        today = datetime.now()

        if today.month == 12:
            next_month = 1
            next_month_year = today.year + 1
        else:
            next_month = today.month + 1
            next_month_year = today.year

        first_day_of_next_month = datetime(next_month_year, next_month, 15)
        expired_date = first_day_of_next_month.strftime('%Y-%m-%d')
        if verify:
            check_username = UserAuth.objects.filter(username=username)
            check_email = UserAuth.objects.filter(email=email)
            if re.search(r'[^a-z0-9_.]', username):
                messages.info(request, "Invalid username format.")
                return render(request,'user_auth/signup.html', user_input_data)
            if len(username) > 10:
                messages.info(request, "username will be 5-10 character")
                return render(request,'user_auth/signup.html', user_input_data)
            if check_username:
                messages.info(request, "username already exist.")
                return render(request,'user_auth/signup.html', user_input_data)
            if len(username)>10 and len(username)< 5:
                messages.info(request, "username will be 5-10 character")
                return render(request,'user_auth/signup.html', user_input_data)
            if check_email:
                messages.info(request, "email already exist.")
                return render(request,'user_auth/signup.html', user_input_data)
            if password != confirm_password:
                messages.info(request, "password is not match.")
                return render(request,'user_auth/signup.html', user_input_data)
            
        else:
            messages.warning(request, "Invalid recaptcha, try again")
            return render(request,'user_auth/signup.html', user_input_data)
    
    return render(request,'user_auth/signup.html', user_input_data)



def verify_email(request):
    if request.method == "GET":
        return render(request,'user_auth/verify_email.html')
    if request.method == "POST":
        email = request.POST['temp_mail']
        verify_code = request.POST['verify_code']
        user_otp = Otp.objects.filter(user_email=email,otp=verify_code)
        if user_otp:
            user = UserAuth.objects.get(email=email)
            user.is_active=True
            user.save()
            messages.success(request, 'Email verification successfull.')
            subject = 'Welcome to Minerflick'
            from_email = formataddr(("MinerFlick", settings.EMAIL_HOST_USER))
            to = user.email
            html_content = render_to_string('email_template/welcome_email.html',{'user':user.username})
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect('login')
        else:
            messages.success(request, 'Invalid Code! Try again.')
            return redirect('login')



def reset_pass(request):
    if request.method == "GET":
        return render(request,"user_auth/reset.html")
        
    
    if request.method == "POST":
        email = request.POST['email']
        data ={
            "email":email
        }
        if '@' not in email:
            messages.warning(request, 'Invalid email address.')
            return render(request,"user_auth/reset.html")
        selected_user = UserAuth.objects.get(email=email)
        if not selected_user:
            messages.warning(request, 'No user found with this email !')
            return render(request,"user_auth/reset.html",context=data)
        user_otp = random.randint(100000,999999)

        subject = 'Reset Password'
        from_email = formataddr(("MinerFlick", settings.EMAIL_HOST_USER))
        to = email
        html_content = render_to_string('email_template/welcome.html',{'generated_code':user_otp})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject,text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, 'Success ! verification code send.')
        return render(request,"user_auth/reset.html",context=data)


def chk_verification_code(request):
    email = request.POST['temp_mail']
    verify_code = request.POST['verify_code']
    data = {
        'email':email
    }
    if email == '':
        messages.warning(request, 'Enter valid email address.')
        return render(request,"user_auth/reset.html")



def update_password(request):
    email = request.POST['temp_mail']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    data = {
        'email':email
    }
    if password == confirm_password:
        user=UserAuth.objects.filter(email=email)
        if user:
            user=UserAuth.objects.get(email=email)
            user.password=password
            user.save()
            messages.success(request, 'Successfully reset Password.')
            return redirect('login')
    else:
        messages.warning(request, 'Password not match.')
        return render(request,"user_auth/change_pass.html",context=data)
    return render(request,"user_auth/reset.html")

@login_required
def signout(request):
    logout(request)
    return redirect('login')
