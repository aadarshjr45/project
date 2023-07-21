from django.db import models
from django.contrib.auth.models import AbstractUser


BOOL_CHOICES = ((True,'Yes'),(False,'No'))

class User(AbstractUser):
#  is_applicant = models.BooleanField(default=True)     
    image = models.ImageField(upload_to='profile/', null=True, blank=True)   
    is_employer = models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True)
    resume = models.FileField(upload_to='resume/', null=True, blank=True)


 

 

