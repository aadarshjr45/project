from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.db import transaction


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


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class" : "form-control"
            }
        ) 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class" : "form-control"
            }
        ) 
    )


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

