from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import therapist_required
from .forms import RegisterForm, PersonalDetailsForm, ProDetailsForm, AddServiceForm, TherapistServiceForm
from .models import Therapist, TherapistService
from core.models import Service


@therapist_required
def home(request):
    # fetch current therapist instance
    if request.user.is_authenticated:
        try:
            therapist = Therapist.objects.get(user=request.user)
        except Therapist.DoesNotExist:
            therapist = None
    else:
        therapist = None
    # render 
    return render(request, 'therapists/home.html', {'therapist': therapist})

@therapist_required
def notifications(request):
    return render(request, 'therapists/notifications.html')

@therapist_required
def schedule(request):
    return render(request, 'therapists/schedule.html')

def about(request):
    return render(request, 'core/about.html', {
        'base_template': 'therapists/base.html'
    })


@login_required
def profile(request, section='personal_details'):
    therapist = get_object_or_404(Therapist, user=request.user)

    personal_form = None
    pro_form = None
    password_form = None

    if section == 'service_settings':
        # Call service_settings() using the therapist.id
        return service_settings(request, therapist.id)

    if request.method == 'POST':
        if section == 'personal_details':
            personal_form = PersonalDetailsForm(request.POST, request.FILES, instance=therapist)
            if personal_form.is_valid():
                personal_form.save()
                messages.success(request, 'Personal details updated successfully.')
        elif section == 'professional_details':
            pro_form = ProDetailsForm(request.POST, instance=therapist)
            if pro_form.is_valid():
                pro_form.save()
                messages.success(request, 'Professional details updated successfully.')
        elif section == 'privacy_security':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                messages.success(request, 'Password changed successfully.')
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                
    else:
        if section == 'personal_details':
            personal_form = PersonalDetailsForm(instance=therapist)
        elif section == 'professional_details':
            pro_form = ProDetailsForm(instance=therapist)
        elif section == 'privacy_security':
            password_form = PasswordChangeForm(request.user)

    return render(request, 'therapists/profile.html', {
        'base_template': 'therapists/base.html',
        'section': section,
        'personal_form': personal_form,
        'pro_form': pro_form,
        'password_form': password_form,
        'therapist': therapist
    })


@login_required
def service_settings(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    
    if request.method == 'POST':
        service_form = AddServiceForm(request.POST, therapist=therapist)
        if service_form.is_valid():
            if 'select_service' in request.POST:
                # Service selected, reinitialize form with prices
                service = service_form.cleaned_data['service']
                service_form = AddServiceForm(therapist=therapist, initial={'service': service})
                # Create a new TherapistService instance
                therapist_service = service_form.save(commit=False)
                therapist_service.therapist = therapist
                therapist_service.service = service  # Ensure service is assigned
                therapist_service.base_price = service.base_price  # Copy base_price
                therapist_service.prices = service.prices  # Copy prices
                therapist_service.save()
                # For now, just redirect to the same page
                return redirect('therapists:profile', section='service_settings')
        else:
            print(f"Form errors: {service_form.errors}")  # Debug statement

        # Handle saving changes to existing services
        for service in TherapistService.objects.filter(therapist=therapist):
            form = TherapistServiceForm(request.POST, service_instance=service)
            if form.is_valid():
                prices = []
                for duration, price_dict in service.prices:
                    new_price_dict = {}
                    for customer_type in price_dict.keys():
                        field_name = f'price_{service.id}_{duration}_{customer_type}'
                        price = form.cleaned_data[field_name]
                        # Convert to int if whole number
                        if price == int(price):
                            price = int(price)
                        new_price_dict[customer_type] = price
                    prices.append([duration, new_price_dict])
                service.prices = prices
                service.save()
                print(f"Updated Service: {service.service.name}")  # Debug statement
    else:
        service_form = AddServiceForm(therapist=therapist)
    
    # Get all services for the therapist
    therapist_services = TherapistService.objects.filter(therapist=therapist)
    service_forms = [TherapistServiceForm(service_instance=service) for service in therapist_services]
    
    return render(request, 'therapists/profile.html', {
        'section': 'service_settings',
        'service_form': service_form,
        'service_forms': service_forms,
        'therapist': therapist,
    })

@login_required
def delete_service(request, therapist_id, service_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    service_to_delete = get_object_or_404(TherapistService, id=service_id, therapist=therapist)
    service_to_delete.delete()
    return redirect('therapists:profile', section='service_settings')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # Create and save the User instance
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password
            )
            # Log in the user
            login(request, user)
            return redirect('therapists:register_details')  # Ensure this matches the name in urls.py
    else:
        form = RegisterForm()
    return render(request, 'therapists/register.html', {'form': form})


@login_required
def register_details(request):
    # check if user has a therapist profile
    if hasattr(request.user, 'therapist'):
        # If so, redirect to homepage
        return redirect('therapists:home')
    # If not, prompt user with registration form to complete sign up
    else:
        if request.method == 'POST':
            personal_form = PersonalDetailsForm(request.POST, request.FILES)
            pro_form = ProDetailsForm(request.POST)
            # Save forms to db if valid and create therapist instance
            if personal_form.is_valid() and pro_form.is_valid():
                # Combine data from both forms
                therapist_data = {
                    'user': request.user,
                    'first_name': personal_form.cleaned_data['first_name'],
                    'last_name': personal_form.cleaned_data['last_name'],
                    'gender': personal_form.cleaned_data['gender'],
                    'age': personal_form.cleaned_data['age'],
                    'description': personal_form.cleaned_data['description'],
                    'street': personal_form.cleaned_data['street'],
                    'number': personal_form.cleaned_data['number'],
                    'postcode': personal_form.cleaned_data['postcode'],
                    'city': personal_form.cleaned_data['city'],
                    'country': personal_form.cleaned_data['country'],
                    'phone_number': personal_form.cleaned_data['phone_number'],
                    'pronouns': personal_form.cleaned_data['pronouns'],
                    'picture': personal_form.cleaned_data['picture'],
                    'qualifications': pro_form.cleaned_data['qualifications'],
                    'specialties': pro_form.cleaned_data['specialties'],
                    'years_xp': pro_form.cleaned_data['years_xp'],
                    'accepted_customer_groups': pro_form.cleaned_data['accepted_customer_groups'],
                    'provided_equipment': pro_form.cleaned_data['provided_equipment'],
                    'required_equipment': pro_form.cleaned_data['required_equipment'],
                }
                
                # Create and save the Therapist instance
                therapist = Therapist.objects.create(**therapist_data)
                
                messages.success(request, 'Account created successfully! Welcome.')
                return redirect('therapists:home')  # Redirect after saving
        # If not all forms are valid, prompt page again to user
        else:
            personal_form = PersonalDetailsForm()
            pro_form = ProDetailsForm()
        return render(request, 'therapists/register_details.html', {
            'personal_form': personal_form,
            'pro_form': pro_form,
        })

def user_logout(request):
    logout(request)
    return redirect('home')

@therapist_required
def customer_profile(request):
    return render(request, 'customer_profile/profile.html')