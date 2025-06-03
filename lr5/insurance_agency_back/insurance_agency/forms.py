import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Customer, Owner, Employee, Realty, Deal, UserProfile

secrets = {
    "employee": "employee_secret_code",
}


class CustomerForm(forms.ModelForm):
    budget = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Budget must be positive"
    )
    class Meta:
        model = Customer
        fields = ["budget", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Leave some notes about yourself..."}),
        }


class CustomerAdminForm(forms.ModelForm):
    budget = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Budget must be positive"
    )
    user = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    class Meta:
        model = Customer
        fields = ["budget", "notes", "is_vip", "user"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Leave some notes about yourself..."}),
        }


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["preferred_contact_time", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Leave some notes about yourself..."}),
        }


class EmployeeAdminForm(forms.ModelForm):
    work_experience = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Work experience must be positive"
    )
    class Meta:
        model = Employee
        fields = ["work_type", "work_experience", "image", "user"]
        widgets = {
           "work_type": forms.Select(),
            "user": forms.Select()
        }


class EmployeeForm(forms.ModelForm):
    work_experience = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Work experience must be positive"
    )
    secret_code = forms.CharField(
        help_text="The confirmation code that you are an employee",
        max_length=20
    )
    class Meta:
        model = Employee
        fields = ["work_type", "work_experience", "image"]
        widgets = {
           "work_type": forms.Select(),
        }

    def clean_secret_code(self):
        secret_code = self.cleaned_data['secret_code']
        if secret_code != secrets["employee"]:
            raise forms.ValidationError("Secret codes mismatches. You are not employee")
        return secret_code


class RealtyForm(forms.ModelForm):
    price = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Price must be positive"
    )
    area = forms.DecimalField(
        validators=[MinValueValidator(0)],
        help_text="Area must be positive"
    )
    built_year = forms.DecimalField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.date.today().year)],
        help_text=f"Build year must be positive and less than {datetime.date.today().year}"
    )
    class Meta:
        model = Realty
        fields = ["type", "name", "address", "price",
                  "area", "built_year", "photo"]
        widgets = {
            "type": forms.Select(),
        }


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["deal_type"]
        widgets = {
            "deal_type": forms.Select(),
        }


class DealAdminForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["deal_type", "status", "realty", "customer"]
        widgets = {
            "deal_type": forms.Select(),
            "status" : forms.Select(),
            "realty": forms.Select(),
            "customer": forms.Select(),
        }


class DealUpdateForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ["status", "actual_end_date"]
        widgets = {
            "status": forms.Select(),
            "actual_end_date": forms.DateInput(attrs={'type': 'date'}),
        }