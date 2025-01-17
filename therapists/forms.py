from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Therapist


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

# Registration detailed form
class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = ['name', 'gender', 'description', 'address', 'phone_number', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 42}),
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
    
    class Meta:
        model = Therapist
        fields = ['years_xp', 'equipment_pref']
        widgets = {
            'equipment_pref': forms.Textarea(attrs={'placeholder': 'Enter your equipment preferences', 'class': 'input-field', 'rows': 8, 'cols': 72}),
        }

        labels = {
            'years_xp': 'Years of Experience',
            'equipment_pref': 'Equipment Preferences'
        }


# Empty placeholder form
class EmptyForm(forms.Form):
    pass
