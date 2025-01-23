from django.shortcuts import render, redirect, get_object_or_404
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
    notifications = Notification.objects.filter(recipient=user).order_by('-created_at')

    # fetch notifications sent to all local therapists
    if hasattr(user, 'therapist'):
        therapist = user.therapist
        city_notifications = Notification.objects.filter(city=therapist.city)
        notifications = notifications.union(city_notifications).order_by('-created_at')
        template_name = 'therapists/notifications.html'
    else:
        template_name = 'customers/notifications.html'

    return render(request, template_name, {'notifications': notifications})