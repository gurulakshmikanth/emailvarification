from django import forms
from .models import User

class Registrationform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['email','password']


class OTPVerificationform(forms.Form):#regural form
    email=forms.EmailField()
    otp=forms.CharField(max_length=6)