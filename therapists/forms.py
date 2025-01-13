from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Therapist
from core.models import NumberOfCustomers


# initial registration form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data

# Registration detailed form
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['name', 'gender', 'description', 'address', 'phone_number', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 36}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'class': 'input-field', 'rows': 4, 'cols': 36}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'input-field'}),

        }
        labels = {
            'name': 'Your name',
            'gender': 'Your gender',
            'description': 'Description',
            'address': 'Address',
            'phone_number': 'Phone Number',
        }


class ProDetailsForm(forms.ModelForm):
    number_of_customers = forms.ModelMultipleChoiceField(
        queryset=NumberOfCustomers.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True  # Ensure that this field is required
    )
    
    class Meta:
        model = Therapist
        fields = ['number_of_customers', 'years_xp']
        widgets = {
            'number_of_customers': forms.SelectMultiple(attrs={'class': 'select-field'}),
        }

        labels = {
            'number_of_customers': 'Number of Customers' ,
            'years_xp': 'Years of Experience'
        }


# Empty placeholder form
class EmptyForm(forms.Form):
    pass