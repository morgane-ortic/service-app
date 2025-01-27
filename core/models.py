from django.db import models
from django.apps import apps
from django.contrib.auth.models import User


class AcceptedCustomerGroups(models.Model):
    """Enables multiple choices to be selected at once"""
    CHOICES = [
        ('single', 'Single'),
        ('couple', 'Couple'),
        ('group', 'Group'),
    ]
    choice = models.CharField(max_length=30, choices=CHOICES)

    class Meta:
        verbose_name = "Accepted Customer Group"
        verbose_name_plural = "Accepted Customer Groups"

    def __str__(self):
        return self.choice

    

class Booking(models.Model):
    # Status choices for the booking
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, related_name='booking')
    therapist = models.ForeignKey('therapists.Therapist', on_delete=models.SET_NULL, null=True, related_name='booking')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, related_name='booking')
    number_of_customers = models.PositiveIntegerField(default=1)  # Directly store the number of customers as an integer
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    booking_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    prices = models.JSONField(default=list)

    # Status field to track the state of the booking
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',  # Default status is active
    )

    def __str__(self):
        # Format the booking's string representation
        formatted_date_time = self.booking_date_time.strftime("%Y-%m-%d %H:%M")
        customer_username = (
            self.customer.user.username if self.customer and self.customer.user else "No customer assigned"
        )
        therapist_username = (
            self.therapist.user.username if self.therapist and self.therapist.user else "No therapist assigned"
        )
        return (
            f'Booking ID: {self.id}\n'
            f'Customer: {customer_username}\n'
            f'Therapist: {therapist_username}\n'
            f'Booking Time: {formatted_date_time}\n'
            f'Status: {self.get_status_display()}\n'
        )


    



class ServiceType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Each type must be unique

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    prices = models.JSONField(default=list)
    picture = models.ImageField(upload_to='service_pictures/')  # For uploading pictures
    service_types = models.ManyToManyField(ServiceType, related_name="services")  # Don't remove this line, it is needed in services.html for the sidebar with pink options

    def __str__(self):
        return self.name

    def get_price(self, duration, customer_type):
        """
        Retrieve the price for a given duration and customer type.

        :param duration: str, e.g., "60", "90", "120"
        :param customer_type: str, e.g., "single", "couple", "group"
        :return: decimal.Decimal or None if not found
        """
        for entry in self.prices:
            if str(entry[0]) == duration:  # Match the duration
                return entry[1].get(customer_type)  # Return the price for the specified customer type
        return None  # Return None if no matching duration or customer type is found


class Notification(models.Model):
    # each notification has EITHER a recipient (individual) or city (all local therapists)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    message = models.TextField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        if self.recipient:
            return f"Notification for {self.recipient.username}: {self.message[:20]}"
        elif self.booking and self.booking.city:
            return f"Notification for city {self.booking.city}: {self.message[:20]}"
        else:
            return f"Notification: {self.message[:20]}"

    @classmethod
    def send_notification(cls, message, recipient=None, city=None):
        # Importing Therapist model here to avoid circular import
        Therapist = apps.get_model('therapists', 'Therapist')
        if recipient:
            # Send notification to a specific user
            cls.objects.create(recipient=recipient, message=message)
        elif city:
            # Send notification to all therapists in the specified city
            therapists_in_city = Therapist.objects.filter(city=city)
            for therapist in therapists_in_city:
                cls.objects.create(recipient=therapist.user, message=message, booking__city=city)