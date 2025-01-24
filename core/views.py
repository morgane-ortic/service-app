from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.http import JsonResponse
from core.models import Booking, Notification


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Pass request and data to the form
        if form.is_valid():
            user = form.get_user()  # Get the authenticated user from the form
            login(request, user)
            # redirect to main app home url
            return redirect('home')
        else:
            form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {
        'base_template': 'customers/base.html',
        'form': form
    })

def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = "cancelled"
        booking.save()

        # Render the booking for history (optional)
        return JsonResponse({"success": True, "html": render_to_string("booking_history_item.html", {"booking": booking})})

    return JsonResponse({"success": False, "error": "Invalid request method"}, status=400)


@login_required
def display_notifications(request):
    user = request.user

    if hasattr(user, 'therapist'):
        therapist = user.therapist
        bookings = Booking.objects.filter(therapist=therapist)
        template_name = 'therapists/notifications.html'
        # Fetch notifications for the therapist's city
        city_notifications = Notification.objects.filter(
            booking__city__iexact=therapist.city
        ).annotate(booking_created_at=F('booking__created_at')).order_by('-booking_created_at')
    
    else:
        bookings = Booking.objects.filter(customer__user=user)
        template_name = 'customers/notifications.html'
        city_notifications = Notification.objects.none()

    # Fetch notifications for the user
    user_notifications = Notification.objects.filter(recipient=user).order_by('-booking__created_at')

    # If the user is a therapist, also fetch notifications for the bookings
    if hasattr(user, 'therapist'):
        booking_notifications = Notification.objects.filter(booking__in=bookings).order_by('-booking__created_at')
        notifications = (user_notifications | booking_notifications | city_notifications).distinct().order_by('-booking__created_at')
    else:
        notifications = user_notifications

    # Debugging statements
    print(f"User: {user}")
    print(f"User Type: {'Therapist' if hasattr(user, 'therapist') else 'Customer'}")
    print(f"Bookings: {bookings}")
    print(f"Notifications: {notifications}")

    return render(request, template_name, {'notifications': notifications})