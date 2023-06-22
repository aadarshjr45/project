from django.db import models
from django.contrib.auth.models import AbstractUser


BOOL_CHOICES = ((True,'Yes'),(False,'No'))

class User(AbstractUser):
#  is_applicant = models.BooleanField(default=True)     
    image = models.ImageField(upload_to='profile/', null=True, blank=True)   
    is_employer = models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True)


 

 


    # user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, related_name='applicant')
  

# class Employer(models.Model):
#   user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, related_name='employer')
#   company_name = models.CharField(max_length=255, blank=True, null=True)
#   website = models.CharField(max_length=100, blank=True)
   

