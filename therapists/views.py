from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, PersonalDetailsForm, ProDetailsForm, EmptyForm
from core.forms import LoginForm
from .models import Therapist

# Placeholder views
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

def notifications(request):
    return render(request, 'therapists/notifications.html')

def schedule(request):
    return render(request, 'therapists/schedule.html')

def about(request):
    return render(request, 'core/about.html', {
        'base_template': 'therapists/base.html'
    })

def profile(request, section='personal_details'):
    therapist = get_object_or_404(Therapist, user=request.user)

    if request.method == 'POST':
        if section == 'personal_details':
            personal_form = PersonalDetailsForm(request.POST, request.FILES, instance=therapist)
            if personal_form.is_valid():
                personal_form.save()
        elif section == 'professional_details':
            pro_form = ProDetailsForm(request.POST, instance=therapist)
            if pro_form.is_valid():
                pro_form.save()

    else:
        if section == 'personal_details':
            personal_form = PersonalDetailsForm(instance=therapist)
            pro_form = None
        elif section == 'professional_details':
            pro_form = ProDetailsForm(instance=therapist)
            personal_form = None
        else:
            personal_form = None
            pro_form = None

    return render(request, 'therapists/profile.html', {
        'base_template': 'therapists/base.html',
        'section': section,
        'personal_form': personal_form,
        'pro_form': pro_form
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
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
    if request.method == 'POST':
        personal_form = PersonalDetailsForm(request.POST, request.FILES)
        pro_form = ProDetailsForm(request.POST)
        
        if personal_form.is_valid() and pro_form.is_valid():
            # Save the personal details form
            therapist = personal_form.save(commit=False)
            therapist.user = request.user 
            therapist.save()
            personal_form.save_m2m()  # Save the many-to-many relationships
            
            # Save the professional details form
            pro_details = pro_form.save(commit=False)
            pro_details.therapist = therapist  # Link the professional details to the therapist
            pro_details.save()
            return redirect('therapists:register_confirm')  # Redirect after saving
    else:
        personal_form = PersonalDetailsForm()
        pro_form = ProDetailsForm()
    return render(request, 'therapists/register_details.html', {
        'personal_form': personal_form,
        'pro_form': pro_form,
        'empty_form': EmptyForm
    })


def register_confirm(request):
    return render(request, 'therapists/register_confirm.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Pass request and data to the form
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user from the form
            login(request, user)
            return redirect('home')
        else:
            form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {
        'base_template': 'therapists/base.html',
        'form': form
    })

def user_logout(request):
    logout(request)
    return redirect('home')

def customer_profile(request):
    return render(request, 'customer_profile/profile.html')

def settings(request):
    return render(request, 'therapists/settings.html')