from ast import mod
from tkinter import N
from turtle import bk, mode
from django.db import models
from users.models import User
from django.core.validators import FileExtensionValidator
from employer.models import Company


class Salary(models.TextChoices):
    NONE = "None", "Select Salary Range"
    FIRST = "10000-20000","10000-20000"
    SECOND = "20000-30000","20000-30000"
    THIRD = "30000-40000","30000-40000"
    FOURTH = "40000-50000","40000-50000"
    FIFTH = "50000-60000","50000-60000"
    SIXTH = "60000-70000","60000-70000"
    SEVENTH = "70000-80000","70000-80000"
    EIGHTH = "80000-90000","80000-90000"
    NINTH = "90000-100000","90000-100000"

class Category(models.TextChoices):

    NONE = "None", "Select One Category"
    FREELANCER = "Free Lancer","Free Lancer"
    PARTTIME = "Part Time","Part Time"
    FULLTIME = "Full Time", "Full Time"
    INTERN = "Intern", "Intern"
    TEMPORARY = "Temporary", "Temporary"
    CONTRACT = "Contract", "Contract"

class Level(models.TextChoices):
    NONE = "None", "Select One Level"
    ENTRY = "Entry","Entry"
    MID = "Mid","Mid"
    SENIOR = "Senior", "Senior"
    MANAGER = "Manager", "Manager"


class Type(models.TextChoices):
    NONE = "None", "Select One Type"
    TEACHER = "Teacher","Teacher"
    IT = "IT","IT"
    COMPUTERPROGRAMMER = "Computer Programmer", "Computer Programmer"
    GRAPHICSDESIGNER = "Graphics Designer", "Graphics Designer"
    WEBDEVELOPER ="Web Developer","Web Developer"
    DATABASEADMINISTRATOR ="Database Administrator","Database Administrator"
    TECHNICIAN ="Technician","Technician"
    ACCOUNTANT ="Accountant","Accountant"
    SOFTWAREDEVELOPER="Software Developer","Software Developer"
    WEBDESIGNER="Web Designer","Web Designer"
    HARDWAREENGINEER="Hardware Engineer","Hardware Engineer"
    NETWORKADMINISTRATOR="Network Administrator","Network Administrator"
    HARDWAREARCHITECT="Hardware Architect","Hardware Architect"
    DATAANALYST="Data Analyst","Data Analyst"
    SYSTEMADMINISTRATOR="System Administrator","System Administrator"
    COMPUTERSCIENTIST="Computer Scientist","Computer Scientist"
    SOFTWAREENGINEER="Software Engineer","Software Engineer"
    SYSTEMSECURITY="System Securtiy","System Securtiy"
    MOBILEAPPLICATIONDEVELOPER="Mobile Application Developer","Mobile Application Developer"
    GAMEDESIGNER="Game Designer","Game Designer"
    GAMEDEVELOPER="Game Developer","Game Developer"
    VISUALDEVELOPER="Visual Developer","Visual Developer"
    NETWORKANALYST="Network Analyst","Network Analyst"
    NETWORKMANAGER="Network Manager","Network Manager"
    NETWORKDESIGNER="Network Designer","Network Designer"
    NETWORKENGINEER="Network Engineer","Network Engineer"
    SOFTWARETESTER="Software Tester","Software Tester"
    DATASCIENTIST="Data Scientist","Data Scientist"
    DATAARCHITECT="Data Architect","Data Architect"
    SOFTWAREARCHITECT="Software Architect","Software Architect"
    INFORMATIONARCHITECT="Information Architect","Information Architect"
    STATISTICALPROGRAMMER="Statistical Programmer","Statistical Programmer"
    ITINSTRUCTOR="IT Instructor","IT Instructor"
    TEXTUREARTIST="Texture Artist","Texture Artist"
    TECHNICALARTIST="Technical Artist","Technical Artist"
    GAMEDIRECTOR="Game Director","Game Director"
    GAMEPRODUCER="Game Producer","Game Producer"
    ANIMATOR="Animator","Animator"
    ANIMATIONSUPERVISOR="animationsupervisor","Animation Supervisor"
    ITMANAGER="Animation Supervisor","IT Manager"
    WEBMASTER="Web Master","Web Master"
    WENEDITOR="Web Editor","Web Editor"
    CONTENTMANAGER="Content Manager","Content Manager"
    CINEMATICARTIST="Cinematic Artist","Cinematic Artist"
    CHARACTERDESIGNER="Character Designer","Character Designer"
    SUPERVISOR="Supervisor","Supervisor"
    PROFESSIONALGAMER="Profesional Gamer","Profesional Gamer"


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_website = models.CharField(max_length=200, null=True, blank=True)
    logo = models.FileField(upload_to='logo/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg'])])
    location = models.CharField(max_length=201, null=True, blank=True)
    no_of_openings = models.PositiveIntegerField()
    salary = models.CharField(choices=Salary.choices,default=None,max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    application_valid = models.DateField()
    category = models.CharField(choices=Category.choices,default=None)
    type = models.CharField(choices=Type.choices,default=None)
    level = models.CharField(choices=Level.choices,default=None)
    modified_at = models.DateField(auto_now=True)
    posted_by = models.ForeignKey(User,on_delete= models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.title
    


class Status(models.TextChoices):
    PENDING = "Pending","Pending"
    ACCEPTED = "Accepted","Accepted"
    REJECTED = "Rejected", "Rejected"


class Application(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255,null=True, blank=True)
    resume = models.FileField(upload_to='resume/',null=True,blank=True,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    submitted_on = models.DateField(auto_now=True)
    posted_by = models.CharField(max_length=200, null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_for = models.ForeignKey(Job,on_delete=models.CASCADE) 
    status = models.CharField(choices=Status.choices,default=Status.PENDING)

    def __str__(self):
        return self.submitted_for.title
    

class Message(models.Model):
    message = models.CharField(max_length=1055, null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING )
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    applicant_name = models.CharField(max_length=255, null=True, blank=True)
    employer_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.status
    







      
    
        