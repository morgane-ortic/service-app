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
    return render(request, 'therapists/settings.html')