from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse




# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = (
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["name"].widget.attrs["class"] = "form-control"
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control row mb-2 col md-3"


# class ApplicantForm(UserForm):
#     class Meta:
#         model = Applicant
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["name"].widget.attrs["class"] = "form-control"
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control row mb-2 col md-3"


# class EmployerForm(forms.ModelForm):
#     class Meta:
#         model = Employer
#         fields = (
#             "company_name",
#             "website",
#         )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.fields["name"].widget.attrs["class"] = "form-control"
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control row mb-2 col md-3"


# class LoginForm(forms.Form):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "class" : "form-control"
#             }
#         ) 
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={
#                 "class" : "form-control"
#             }
#         ) 
#     )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid Login Credentials")
        return self.cleaned_data
    
    def login(self,request):
        if request.method == "POST":
            
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')

            user = authenticate(username=username,password=password)
            return user



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ( 
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "is_employer",
            "image",
         
            )
        

       

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={ 'placeholder': 'First Name'})
        self.fields['last_name'].widget = forms.TextInput(attrs={ 'placeholder': 'Last Name'})
        self.fields['username'].widget = forms.TextInput(attrs={ 'placeholder': 'Username'})
        self.fields['email'].widget = forms.EmailInput(attrs={ 'placeholder': 'Email'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={ 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={ 'placeholder': 'Password confirmation'})
        self.fields['image'].widget = forms.FileInput(attrs={ 'placeholder': 'Profile Picture'})
       

        
        


        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['username'].label = "Username"
        self.fields['email'].label = "Email"
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"
        self.fields['image'].label = "Profile Picture"
        self.fields['is_employer'].label = "Are you an employer?"



        self.fields['username'].help_text = "Username must be unique."
        self.fields['email'].help_text = "Email must be unique."
        self.fields['password1'].help_text = "Password must be 8 characters or more and not too common"
        
        


        



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            "resume"
            )
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control row-4"



        
        

        

