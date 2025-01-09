from django.shortcuts import render, redirect

from .forms import RegisterDetailsForm

# Placeholder views
def home(request):
    return render(request, 'customers/home.html')

def services(request):
    return render(request, 'customers/services.html')

def bookings(request):
    return render(request, 'customers/bookings.html')

def profile(request):
    return render(request, 'customers/profile.html')

def about(request):
    return render(request, 'core/about.html', {
        'base_template': 'customers/base.html'
    })

def contact(request):
    return render(request, 'core/contact.html', {
        'base_template': 'customers/base.html'
    })

def register(request):
    return render(request, 'customers/register.html')

def register_details(request):
    
    if request.method == 'POST':
        form = RegisterDetailsForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
        if form.is_valid():
            form.save()  # Save the user profile, including the image
            return redirect('registration_confirm')  # Redirect after saving
    else:
        form = RegisterDetailsForm()

    return render(request, 'customers/register_details.html', {'form': form})

def register_confirm(request):
    return render(request, 'customers/register_confirm.html')

def login(request):
    return render(request, 'core/login.html', {
        'base_template': 'customers/base.html'
    })