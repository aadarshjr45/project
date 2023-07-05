from django.db import models
from users.models import User
from django.core.validators import FileExtensionValidator


class Company(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_website = models.CharField(max_length=255, null=True, blank=True)
    company_location = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    logo = models.FileField(upload_to='logo/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])


    def __str__(self):
        return self.company_name
