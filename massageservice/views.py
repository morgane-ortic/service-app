from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from therapists.models import Therapist

# This defines whether the home url points to customer or therapist homepage
# depending whether a therapist is connected or not
def home(request):
    # check if a user is logged in
    if request.user.is_authenticated:
        try:
            # Check if the logged-in user is a therapist
            therapist = Therapist.objects.get(user=request.user)
            return redirect('therapists:home')  # Redirect to therapist's home view
        except Therapist.DoesNotExist:
            return redirect('customers:home')  # Redirect to customer's home view
    else:
        return redirect('customers:home')  # Redirect to customer's home view if no user is logged in