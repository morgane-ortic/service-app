<<<<<<< HEAD
from django.shortcuts import render, redirect

from .forms import RegisterDetailsForm

# Placeholder views
def home(request):
    return render(request, 'therapists/home.html')

def notifications(request):
    return render(request, 'therapists/notifications.html')

def schedule(request):
    return render(request, 'therapists/schedule.html')

def about(request):
    return render(request, 'core/about.html', {
        'base_template': 'therapists/base.html'
    })

def contact(request):
    return render(request, 'core/contact.html', {
        'base_template': 'therapists/base.html'
    })

def profile(request):
    return render(request, 'therapists/profile.html')

def register(request):
    return render(request, 'therapists/register.html')

def register_details(request):
    
    if request.method == 'POST':
        form = RegisterDetailsForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
        if form.is_valid():
            form.save()  # Save the user profile, including the image
            return redirect('registration_confirm')  # Redirect after saving
    else:
        form = RegisterDetailsForm()

    return render(request, 'therapists/register_details.html', {'form': form})

def register_confirm(request):
    return render(request, 'therapists/register_confirm.html')

def login(request):
    return render(request, 'core/login.html', {
        'base_template': 'therapists/base.html'
    })

def customer_profile(request):
    return render(request, 'customer_profile/profile.html')

def settings(request):
=======
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, RegisterDetailsForm
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
    return render(request, 'therapists/profile.html', {
        'base_template': 'therapists/base.html',
        'section': section
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
        form = RegisterDetailsForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
        if form.is_valid():
            therapist = form.save(commit=False)  # Save the form but don't commit to the database yet
            therapist.user = request.user  # Assuming you want to link the therapist to the logged-in user
            therapist.save()  # Now save the therapist instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('therapists:register_confirm')  # Redirect after saving
    else:
        form = RegisterDetailsForm()
    return render(request, 'therapists/register_details.html', {'form': form})


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
>>>>>>> 9f9de84ee02e82ff27984ae7781aa155bd3ce490
    return render(request, 'therapists/settings.html')