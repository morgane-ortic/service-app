from django.shortcuts import render

from django.conf import settings

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
    print(settings.TEMPLATES[0]['DIRS'])
    return render(request, 'core/about.html', {
        'base_template': 'customers/base.html'
    })

def contact(request):
    return render(request, 'core/contact.html', {
        'base_template': 'customers/base.html'
    })

def register(request):
    return render(request, 'customers/register.html')

def login(request):
    return render(request, 'core/login.html', {
        'base_template': 'customers/base.html'
    })