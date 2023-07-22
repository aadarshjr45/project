from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


BOOL_CHOICES = ((True,'Yes'),(False,'No'))

class User(AbstractUser):
#  is_applicant = models.BooleanField(default=True)     
    image = models.ImageField(upload_to='profile/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])   
    is_employer = models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True, default=False)
    resume = models.FileField(upload_to='resume/', null=True, blank=True,validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','pdf'])])


 

 

