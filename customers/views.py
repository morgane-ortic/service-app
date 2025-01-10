from django.shortcuts import render, redirect, get_object_or_404
from core.models import Service, ServiceType
from .forms import RegisterDetailsForm
from django.conf import settings
from django.http import JsonResponse
import stripe


# Placeholder views
def home(request):
    return render(request, 'customers/home.html')

def services(request):
    return render(request, 'customers/services.html')


def bookings(request):
    service_type_name = request.GET.get('service_type', 'all')
    if service_type_name == 'all':
        services = Service.objects.all()
    else:
        try:
            service_type = ServiceType.objects.get(name=service_type_name)
            services = Service.objects.filter(service_types=service_type)
        except ServiceType.DoesNotExist:
            services = Service.objects.none()

    service_types = ServiceType.objects.all()

    return render(request, 'customers/bookings.html', {
        'services': services,
        'service_types': service_types,
        'selected_type': service_type_name,
    })

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'customers/service_detail.html', {'service': service})

# Set your secret key from Stripe Dashboard
stripe.api_key = settings.STRIPE_SECRET_KEY  # Add this key to your settings.py

def create_checkout_session(request):
    try:
        # Create a new Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd20',  # Replace with your currency
                        'product_data': {
                            'name': 'Your Service Name',  # Replace with the dynamic service name
                        },
                        'unit_amount': 5000,  # Amount in cents (e.g., $50.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})








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