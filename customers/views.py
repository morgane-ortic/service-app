from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer
from core.models import Service, ServiceType
from .forms import RegisterForm, RegisterDetailsForm
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



stripe.api_key = settings.STRIPE_SECRET_KEY  # Set your Stripe secret key

def create_checkout_session(request):
    print("create_checkout_session view called")  # Debug print
    ...


def create_checkout_session(request):
    print("create_checkout_session view called")  # Debug print statement

    if request.method != 'POST':
        print("Invalid request method")  # Debug print for invalid method
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        # Create a new Stripe Checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',  # Replace with your valid currency code
                        'product_data': {
                            'name': 'Your Service Name',  # Replace dynamically if needed
                        },
                        'unit_amount': 5000,  # Amount in cents (e.g., $50.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',  # Adjust to match your success page
            cancel_url='http://127.0.0.1:8000/cancel/',    # Adjust to match your cancel page
        )
        print(f"Checkout session created: {session.id}")  # Debug print for successful session creation
        return JsonResponse({'id': session.id})
    except Exception as e:
        print(f"Error creating checkout session: {e}")  # Debug print for exceptions
        return JsonResponse({'error': str(e)}, status=400)










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
            return redirect('customers:register_details')  # Ensure this matches the name in urls.py
    else:
        form = RegisterForm()
    return render(request, 'customers/register.html', {'form': form})


@login_required
def register_details(request):
    if request.method == 'POST':
        form = RegisterDetailsForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
        if form.is_valid():
            customer = form.save(commit=False)  # Save the form but don't commit to the database yet
            customer.user = request.user  # Assuming you want to link the customer to the logged-in user
            customer.save()  # Now save the customer instance
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('customers:register_confirm')  # Redirect after saving
    else:
        form = RegisterDetailsForm()
    return render(request, 'customers/register_details.html', {'form': form})


def register_confirm(request):
    return render(request, 'customers/register_confirm.html')


def user_login(request):
    return render(request, 'core/user_login.html', {
        'base_template': 'customers/base.html'
    })

def user_logout(request):
    logout(request)
    return redirect('home')