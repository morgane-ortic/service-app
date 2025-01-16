from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import therapist_required
from .forms import RegisterForm, PersonalDetailsForm, ProDetailsForm, EmptyForm
from core.forms import LoginForm
from .models import Therapist


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
                    'name': personal_form.cleaned_data['name'],
                    'gender': personal_form.cleaned_data['gender'],
                    'description': personal_form.cleaned_data['description'],
                    'address': personal_form.cleaned_data['address'],
                    'phone_number': personal_form.cleaned_data['phone_number'],
                    'picture': personal_form.cleaned_data['picture'],
                    'years_xp': pro_form.cleaned_data['years_xp'],
                    'equipment_pref': pro_form.cleaned_data['equipment_pref'],
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