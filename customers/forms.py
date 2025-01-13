from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer

class RegisterForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'input-field'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'input-field'}))

class RegisterDetailsForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'description', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 60}),
        }
        labels = {
            'name': 'Your name',
            'gender': 'Your gender',
            'description': 'Description'
        }