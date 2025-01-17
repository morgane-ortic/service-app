from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Therapist
from core.models import AcceptedCustomerGroups


# Initial registration form
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
    accepted_customer_groups = forms.ModelMultipleChoiceField(
        queryset=AcceptedCustomerGroups.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Therapist
        fields = ['first_name', 'last_name', 'gender', 'age', 'pronouns', 'description',
                  'street', 'number', 'postcode', 'city', 'country',
                  'phone_number', 'picture', 'years_xp', 'accepted_customer_groups']
        
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'input-field'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'input-field'}),
                   'gender': forms.Select(attrs={'class': 'select-field'}),
                   'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8, 'cols': 40}),
                   'street': forms.TextInput(attrs={'placeholder': 'Enter your street', 'class': 'input-field'}),
                   'number': forms.TextInput(attrs={'placeholder': 'Enter your house number', 'class': 'input-field'}),
                   'postcode': forms.TextInput(attrs={'placeholder': 'Enter your postcode', 'class': 'input-field'}),
                   'city': forms.TextInput(attrs={'placeholder': 'Enter your city', 'class': 'input-field'}),
                   'country': forms.TextInput(attrs={'placeholder': 'Enter your country', 'class': 'input-field'}),
                   'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'input-field'}),
                   'accepted_customer_groups': forms.SelectMultiple(attrs={'class': 'select-field'}),}

    def __init__(self, *args, **kwargs):
        """
        Sets certain fields as optional.
        """
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['street'].required = False
        self.fields['number'].required = False
        self.fields['postcode'].required = False
        self.fields['city'].required = False
        self.fields['country'].required = False
        self.fields['phone_number'].required = False