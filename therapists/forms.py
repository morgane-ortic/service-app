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