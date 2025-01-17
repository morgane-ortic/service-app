from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Customer
from core.models import Service, ServiceType
from .forms import RegisterForm, RegisterDetailsForm
from core.forms import LoginForm
from django.conf import settings
from django.http import JsonResponse
import stripe
from core.models import Booking


# Placeholder views
def home(request):
    print(f"Host: {request.get_host()}")  # Debugging output

    # fetch current customer instance
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = None
    else:
        customer = None
    # render 
    return render(request, 'customers/home.html', {'customer': customer})

def services(request):
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

    return render(request, 'customers/services.html', {
        'services': services,
        'service_types': service_types,
        'selected_type': service_type_name,
    })
    
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'customers/service_detail.html', {'service': service})

from django.shortcuts import render, redirect
from core.models import Booking

def bookings(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    # Check if the user has a related Customer object
    if not hasattr(request.user, 'customer'):
        return render(request, 'customers/bookings.html', {
            'bookings': [],
            'error': 'No customer profile found for this user. Please contact support.',
        })

    # Fetch the currently logged-in customer's bookings
    customer = request.user.customer
    bookings = Booking.objects.filter(customer=customer).order_by('-booking_date_time')

    # Render the template with the bookings context
    return render(request, 'customers/bookings.html', {'bookings': bookings})



def profile(request):
    return render(request, 'customers/profile.html')

def about(request):
    return render(request, 'core/about.html', {
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
        'base_template': 'customers/base.html',
        'form': form
    })

def user_logout(request):
    logout(request)
    print('logged out')
    return redirect('home')





# Stripe API code ==============================================

stripe.api_key = settings.STRIPE_SECRET_KEY  # Your Stripe secret key

@csrf_exempt
def create_checkout_session(request):
    try:
        # Replace with your dynamic data as needed
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',  # Euro as the currency
                        'product_data': {
                            'name': 'Relaxation Massage',  # Replace with the product/service name
                        },
                        'unit_amount': 5000,  # Replace with the price in cents (€50.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://1a35-185-250-215-99.ngrok-free.app/success/',  # Your success page URL
            cancel_url='https://1a35-185-250-215-99.ngrok-free.app/cancel/',    # Your cancel page URL
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def payment_success(request):
    return render(request, 'customers/success.html')

def payment_cancel(request):
    return render(request, 'customers/cancel.html')
