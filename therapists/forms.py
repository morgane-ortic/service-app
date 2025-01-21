from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Therapist, TherapistService
from core.models import Service


# Initial registration form
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
    picture = forms.ImageField(
        label='Profile Picture',
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=forms.FileInput(attrs={'class': 'input-field'})
    )

    class Meta:
        model = Therapist
        fields = [
            'first_name', 'last_name', 'gender', 'age', 'description',
            'street', 'number', 'postcode', 'city', 'country', 
            'phone_number', 'pronouns', 'picture'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': 'input-field'}),
            'gender': forms.Select(attrs={'class': 'select-field'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Enter your age', 'class': 'input-field'}),
            'description': forms.Textarea(attrs={'placeholder': 'A short description of yourself', 'class': 'input-field', 'rows': 8}),
            'street': forms.TextInput(attrs={'placeholder': 'Street name', 'class': 'input-field'}),
            'number': forms.TextInput(attrs={'placeholder': 'House number', 'class': 'input-field'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode', 'class': 'input-field'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'input-field'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'input-field'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'input-field'}),
            'pronouns': forms.Select(attrs={'class': 'select-field'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'age': 'Age',
            'description': 'Description',
            'street': 'Street',
            'number': 'House Number',
            'postcode': 'Postcode',
            'city': 'City',
            'country': 'Country',
            'phone_number': 'Phone Number',
            'pronouns': 'Preferred Pronouns',
            'picture': 'Profile Picture',
        }


class ProDetailsForm(forms.ModelForm):
    class Meta:
        model = Therapist
        fields = [
            'qualifications', 'specialties', 'years_xp', 
            'accepted_customer_groups', 'provided_equipment', 'required_equipment'
        ]
        widgets = {
            'qualifications': forms.Textarea(attrs={'placeholder': 'List your qualifications', 'class': 'input-field', 'rows': 4}),
            'specialties': forms.Textarea(attrs={'placeholder': 'List your specialties', 'class': 'input-field', 'rows': 4}),
            'years_xp': forms.NumberInput(attrs={'placeholder': 'Years of experience', 'class': 'input-field'}),
            'accepted_customer_groups': forms.CheckboxSelectMultiple(),
            'provided_equipment': forms.Textarea(attrs={'placeholder': 'Equipment you provide', 'class': 'input-field', 'rows': 4}),
            'required_equipment': forms.Textarea(attrs={'placeholder': 'Equipment required from clients', 'class': 'input-field', 'rows': 4}),
        }
        labels = {
            'qualifications': 'Qualifications',
            'specialties': 'Specialties',
            'years_xp': 'Years of Experience',
            'accepted_customer_groups': 'Accepted Customer Groups',
            'provided_equipment': 'Provided Equipment',
            'required_equipment': 'Required Equipment',
        }


class TherapistServiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        widget=forms.Select,
        required=True,
        label='Select Service'
    )

    class Meta:
        model = TherapistService
        fields = ['service']
    
        widgets = {
            'prices': forms.Textarea(attrs={'rows': 3, 'cols': 20}),  # Adjust the size of the input field
        }

    def __init__(self, *args, **kwargs):
        print('Getting therapist instance in form...')
        therapist = kwargs.pop('therapist', None)
        print(f"kwargs: {kwargs}")  # Debug statement
        super().__init__(*args, **kwargs)
        if therapist:
            print(f'Therapist found: {therapist}')
            used_services = TherapistService.objects.filter(therapist=therapist).values_list('service', flat=True)
            self.fields['service'].queryset = Service.objects.exclude(id__in=used_services)

        # Dynamically add fields for each price
        if 'initial' in kwargs and 'service' in kwargs['initial']:
            service = kwargs['initial']['service']
            prices = service.prices
            print(f"Service: {service.name}, Prices: {prices}")  # Debug statement
            for duration, price_dict in prices:
                for customer_type, price in price_dict.items():
                    field_name = f'price_{duration}_{customer_type}'
                    print(f"Adding field: {field_name} with initial value: {price}")  # Debug statement
                    self.fields[field_name] = forms.DecimalField(
                        initial=price,
                        label=f'{duration} minutes - {customer_type.capitalize()}',
                        required=False
                    )

        else:
            print('Service data not found!')

    def save(self, commit=True):
        instance = super().save(commit=False)
        prices = []
        for duration, price_dict in self.instance.service.prices:
            new_price_dict = {}
            for customer_type in price_dict.keys():
                field_name = f'price_{duration}_{customer_type}'
                new_price_dict[customer_type] = self.cleaned_data[field_name]
            prices.append([duration, new_price_dict])
        instance.prices = prices
        if commit:
            instance.save()
        return instance

# Empty placeholder form
class EmptyForm(forms.Form):
    pass
