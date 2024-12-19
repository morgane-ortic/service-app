from django.shortcuts import render

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
    return render(request, 'customers/about.html')

def contact(request):
    return render(request, 'customers/contact.html')

def register(request):
    return render(request, 'customers/register.html')

def login(request):
    return render(request, 'customers/login.html')