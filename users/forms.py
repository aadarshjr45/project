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
        widgets = {
            'is_employer': forms.Select(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ( 
            "first_name",
            "last_name",
            "username",
            "email",
            "image",
            )
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control row-4"


