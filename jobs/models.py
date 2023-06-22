from ast import mod
from tkinter import N
from turtle import bk, mode
from django.db import models
from users.models import User
from django.core.validators import FileExtensionValidator

class Category(models.TextChoices):
    FREELANCER = "freelancer","Freelancer"
    PARTTIME = "parttime","Parttime"
    FULLTIME = "fulltime", "Fulltime"
    INTERN = "intern", "Intern"

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    company_website = models.CharField(max_length=200)
    logo = models.FileField(upload_to='logo/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])
    location = models.CharField(max_length=201)
    salary = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    application_valid = models.DateField(blank=True, null=True)
    category = models.CharField(choices=Category.choices,default=Category.FULLTIME)
    modified_at = models.DateField(auto_now=True)
    posted_by = models.ForeignKey(User,on_delete= models.CASCADE, default=1)

    def __str__(self):
        return self.title
    


class Status(models.TextChoices):
    PENDING = "pending","Pending"
    ACCEPTED = "accepted","Accepted"
    REJECTED = "rejected", "Rejected"


class Application(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    resume = models.FileField(upload_to='resumes/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    submitted_on = models.DateField(auto_now=True)
    posted_by = models.CharField(max_length=200, null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    submitted_for = models.ForeignKey(Job,on_delete=models.CASCADE, default=1) 
    status = models.CharField(choices=Status.choices,default=Status.PENDING)

    def __str__(self):
        return self.submitted_for.title
    

class Message(models.Model):
    message = models.CharField(max_length=1055, null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING )
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


class Company(models.Model):
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_website = models.CharField(max_length=255, null=True, blank=True)
    company_location = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    logo = models.FileField(upload_to='logo/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])


    def __str__(self):
        return self.company_name

      
    
        