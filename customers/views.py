from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import customer_required
from .models import Customer
from core.models import Service, ServiceType
from .forms import RegisterForm, PersonalDetailsForm
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt


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

@customer_required
def bookings(request):
    return render(request, 'customers/bookings.html')

@customer_required
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

@customer_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'customers/service_detail.html', {'service': service})

def bookings(request):
    return render(request, 'customers/bookings.html')

@login_required
@customer_required
def profile(request):
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            messages.success(request, 'Password changed successfully.')
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            
        personal_form = PersonalDetailsForm(request.POST, request.FILES, instance=customer)
        if personal_form.is_valid():
            personal_form.save()
            messages.success(request, 'Profile details updated successfully.')
            return redirect('customers:profile')
    else:
        personal_form = PersonalDetailsForm(instance=customer)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'customers/profile.html', {
        'personal_form': personal_form,
        'password_form': password_form,
        'customer': customer
        })

def about(request):
    return render(request, 'core/about.html', {
        'base_template': 'customers/base.html'
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            login(request, user)
            return redirect('customers:register_details')  # Ensure this matches the name in urls.py
    else:
        form = RegisterForm()
    return render(request, 'customers/register.html', {'form': form})

@login_required
def register_details(request):
    # check if user has a therapist profile
    if hasattr(request.user, 'customer'):
        # If so, redirect to homepage
        return redirect('customers:home')
    # If not, prompt user with registration form to complete sign up
    else:
        if request.method == 'POST':
            form = PersonalDetailsForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
            if form.is_valid():
                customer = form.save(commit=False)  # Save the form but don't commit to the database yet
                customer.user = request.user  # Assuming you want to link the customer to the logged-in user
                customer.save()  # Now save the customer instance
                form.save_m2m()  # Save the many-to-many relationships
                messages.success(request, 'Account created successfully! Welcome.')
                return redirect('customers:home')  # Redirect after saving
        else:
            form = PersonalDetailsForm()
        return render(request, 'customers/register_details.html', {'form': form})
    

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
