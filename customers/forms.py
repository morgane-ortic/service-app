from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer


# initial registration form
class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PersonalDetailsForm(forms.ModelForm):
    
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

    def __init__(self, *args, **kwargs):
        '''Sets the following fields as optional'''
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['description'].required = False
        self.fields['picture'].required = False
