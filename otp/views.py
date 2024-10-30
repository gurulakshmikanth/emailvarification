from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
import random
import string
from .models import User
from .forms import *

# Create your views here.

def genetaed_otp(length=6):
    return ''.join(random.choices(string.digits,k=length))

def send_otp_via_email(user):
    otp=genetaed_otp()
    user.otp=otp
    user.otp_created_at=timezone.now()
    user.save()

    #send mail
    subject='Your OTP CODE'
    message=f'Your otp code is {otp}.IT will expire in 5 minutes'
    send_mail(subject,message,'gurukanth0987@gamil.com',[user.email],fail_silently=False,)

def registration(request):
    if request.method=='POST':
        form=Registrationform(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')

            if User.objects.filter(email=email).exists():
                messages.error(request,'User with this email already exists.')
            else:
                user=User.objects.create(email=email,password=password)
                send_otp_via_email(user)
                messages.success(request,'User Registred.Please verify the OTP sent to your email.')
                return redirect('verify_otp')
    else:
        form=Registrationform()
    return render(request,'registration.html',{'form':form})


def verify_otp(request):
    if request.method=='POST':
        form=OTPVerificationform(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            otp=form.cleaned_data.get('otp')

            try:
                user=User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request,'Invalid email')
                return redirect('verify_otp')
            
            if user.otp==otp and user.is_otp_valid():
                user.is_active=True
                user.otp=None # clearr otp after successfully verification
                user.save()
                messages.success(request,'OTP verified successfully.You can now login.')
                return HttpResponse('success')
            else:
                messages.error(request,'Invalid or expire OTP')
    else:
        form=OTPVerificationform()
    return render(request,'verify_otp.html',{'form':form})