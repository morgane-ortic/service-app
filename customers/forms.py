from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer


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

class RegisterDetailsForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'description', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 40}),
        }
        labels = {
            'name': 'Your name',
            'gender': 'Your gender',
            'description': 'Description'
        }