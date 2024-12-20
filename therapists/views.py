from django.shortcuts import render

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

def login(request):
    return render(request, 'core/login.html', {
        'base_template': 'therapists/base.html'
    })

def customer_profile(request):
    return render(request, 'customer_profile/profile.html')

