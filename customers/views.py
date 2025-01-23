from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import customer_required
from .models import Customer
from core.models import Service, ServiceType, Booking
from .forms import RegisterForm, PersonalDetailsForm
from django.conf import settings
from django.http import JsonResponse
import stripe
from customers.models import Customer
from django.utils.timezone import now  # Import 'now' for date comparison

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

from django.utils.timezone import now
from django.db.models import Q

@customer_required
def bookings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        customer = Customer.objects.get(user=request.user)

        # Update the status of bookings that have passed their booking_date_time to "completed"
        Booking.objects.filter(
            customer=customer,
            status='active',
            booking_date_time__lt=now()
        ).update(status='completed')

        # Fetch past bookings (history)
        past_bookings = Booking.objects.filter(
            customer=customer,
            status__in=['completed', 'cancelled']
        ).select_related('therapist', 'service__service').order_by('-booking_date_time')

        # Fetch active bookings (future bookings)
        active_bookings = Booking.objects.filter(
            customer=customer,
            status='active',
            booking_date_time__gte=now()
        ).select_related('therapist', 'service__service').order_by('booking_date_time')

        # Retrieve the current booking data from the session, if available
        current_booking = request.session.get('current_booking', None)

    except Customer.DoesNotExist:
        past_bookings = []
        active_bookings = []
        error_message = 'No customer profile found for this user. Please contact support.'

        return render(request, 'customers/bookings.html', {
            'past_bookings': past_bookings,
            'active_bookings': active_bookings,
            'current_booking': None,
            'error': error_message,
        })

    return render(request, 'customers/bookings.html', {
        'past_bookings': past_bookings,
        'active_bookings': active_bookings,
        'current_booking': current_booking,
    })

@csrf_exempt
def cancel_booking(request, booking_id):
    if request.method == "POST":
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        # Get the booking object
        booking = get_object_or_404(Booking, id=booking_id, customer__user=request.user)

        # Update the booking's status to "cancelled"
        booking.status = "cancelled"
        booking.save()

        return JsonResponse({"success": True, "message": "Booking cancelled successfully."})
    
    return JsonResponse({"error": "Invalid request method."}, status=400)

def get_addresses(request):
    if request.user.is_authenticated:
        addresses = Booking.objects.filter(customer__user=request.user).values_list('address', flat=True).distinct()
        return JsonResponse(list(addresses), safe=False)
    return JsonResponse({"error": "Unauthorized"}, status=401)

@login_required
def get_current_booking(request):
    if request.user.is_authenticated:
        response_data = {}

        # Fetch therapists associated with the user's bookings
        bookings = Booking.objects.filter(customer__user=request.user).select_related('therapist__user')
        therapist_names = []

        for booking in bookings:
            if booking.therapist and booking.therapist.user:
                therapist_names.append(
                    f"{booking.therapist.user.first_name} {booking.therapist.user.last_name}"
                )

        # Remove duplicates and add "No Selected Therapist" as the first option
        unique_therapists = [" - "] + sorted(set(therapist_names))
        response_data["therapists"] = unique_therapists

        return JsonResponse(response_data)

    return JsonResponse({"error": "Unauthorized"}, status=401)




def services(request):
    service_type_name = request.GET.get('service_type', 'all')

    # Fetch services based on the service type filter
    if service_type_name == 'all':
        services = Service.objects.all()
    else:
        try:
            service_type = ServiceType.objects.get(name=service_type_name)
            services = Service.objects.filter(service_types=service_type)
        except ServiceType.DoesNotExist:
            services = Service.objects.none()

    service_types = ServiceType.objects.all()

    # Handle saving booking details via POST request
    if request.method == 'POST':
        # Extract booking details from the form data
        booking_data = {
            "service_name": request.POST.get("service_name"),
            "duration": request.POST.get("duration"),
            "therapist": request.POST.get("therapist"),
            "people_count": request.POST.get("people_count"),
            "date": request.POST.get("date"),
            "time": request.POST.get("time"),
            "city": request.POST.get("city"),
            "country": request.POST.get("country"),
            "payment_method": request.POST.get("payment_method"),
        }

        # Save the booking data in the session
        request.session["current_booking"] = booking_data

        # Redirect to the bookings page
        return redirect("customers:bookings")

    return render(request, 'customers/services.html', {
        'services': services,
        'service_types': service_types,
        'selected_type': service_type_name,
    })

@customer_required
def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'customers/service_detail.html', {'service': service})

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
