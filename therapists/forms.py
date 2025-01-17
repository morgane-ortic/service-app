from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Therapist
from core.models import AcceptedCustomerGroups


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
class RegisterDetailsForm(forms.ModelForm):
    number_of_customers = forms.ModelMultipleChoiceField(
        queryset=NumberOfCustomers.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True  # Ensure that this field is required
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