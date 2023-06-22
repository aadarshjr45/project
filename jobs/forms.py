from cgitb import text
from dataclasses import fields
from click import style
from django import forms
from django.urls import include
from jobs.models import Job, Application
from django.utils import timezone
from django.core.exceptions import ValidationError
from upload_validator import FileTypeValidator, magic


class JobForms(forms.ModelForm):

    class Meta:
        model = Job
        exclude = ('posted_by', 'company_name', 'location', 'company_website', 'logo')

        title = forms.CharField(label="Title",help_text="Title for the job")

        widgets = {
           'application_valid' : forms.DateInput(attrs={'type':'date'}),
           'description': forms.Textarea(attrs={'rows': 5, 'cols': 20,}),
          
           
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean_application_valid(self):
        date = self.cleaned_data.get('application_valid')
        if date < timezone.now().date():
            raise ValidationError("Date cannot be set in past")
        return date

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            'resume' : forms.FileField(
                label='', help_text="Only pdf formats are accepted.", required=False,
                validators=[FileTypeValidator(
                allowed_types=[ 'applcation/pdf'],
                allowed_extensions = ['.pdf'],
            )]
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FilterForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['category']