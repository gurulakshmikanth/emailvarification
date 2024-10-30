from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
from datetime import timedelta

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("User musht have an email adderss")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_superuser(email,password,**extra_fields)

class User(AbstractBaseUser):
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=False)
    otp=models.CharField(max_length=6,blank=True,null=True)
    otp_created_at=models.DateTimeField(auto_now_add=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]


    def is_otp_valid(self):
        expiration_time=self.otp_created_at+timedelta(minutes=5)
        return timezone.now() <= expiration_time