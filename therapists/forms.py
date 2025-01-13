<<<<<<< HEAD
from django import forms
from .models import Therapist
from core.models import NumberOfCustomers

# Registration form
class RegisterDetailsForm(forms.ModelForm):
    number_of_customers = forms.ModelMultipleChoiceField(
        queryset=NumberOfCustomers.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-field'}),
        required=True  # Ensure that this field is required
    )
    
    class Meta:
        model = Therapist
        fields = ['name', 'gender', 'description', 'address', 'phone_number', 'picture', 'years_xp', 'number_of_customers']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 60}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'class': 'input-field', 'rows': 5, 'cols': 40}),
            'phone-number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'input-field'}),
            'number_of_customers': forms.SelectMultiple(attrs={'class': 'select-field'}),

        }
        labels = {
            'name': 'Your name',
            'gender': 'Your gender',
            'description': 'Description',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'years_xp': 'Years of Experience',
            'number_of_customers': 'Number of Customers' 
        }
=======
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
class RegisterDetailsForm(forms.ModelForm):
    number_of_customers = forms.ModelMultipleChoiceField(
        queryset=NumberOfCustomers.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True  # Ensure that this field is required
    )
    
    class Meta:
        model = Therapist
        fields = ['name', 'gender', 'description', 'address', 'phone_number', 'picture', 'years_xp', 'number_of_customers']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 40}),
            'address': forms.Textarea(attrs={'placeholder': 'Enter your address', 'class': 'input-field', 'rows': 5, 'cols': 40}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'input-field'}),
            'number_of_customers': forms.SelectMultiple(attrs={'class': 'select-field'}),

        }
        labels = {
            'name': 'Your name',
            'gender': 'Your gender',
            'description': 'Description',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'years_xp': 'Years of Experience',
            'number_of_customers': 'Number of Customers' 
        }

    def __init__(self, *args, **kwargs):
        '''Sets the following fields as optional'''
        super(RegisterDetailsForm, self).__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['address'].required = False
        self.fields['phone_number'].required = False
>>>>>>> 9f9de84ee02e82ff27984ae7781aa155bd3ce490
