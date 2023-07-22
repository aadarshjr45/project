from django import forms
from employer.models import Company
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import User

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ('added_by',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["id"] = "exampleFormControlInput1"

    def clean_application_valid(self):
        print("hrtr")
        date = self.cleaned_data.get('application_valid')
        if date < timezone.now().date():
            raise ValidationError("Date cannot be set in past")
        return date
    
class EmployerForm(forms.ModelForm):
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