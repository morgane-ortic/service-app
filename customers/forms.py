from django import forms
from django.contrib.auth.models import User
from .models import Customer


# initial registration form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

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