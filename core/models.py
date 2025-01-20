from django.db import models


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
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True, related_name='booking')
    therapist = models.ForeignKey('therapists.Therapist', on_delete=models.SET_NULL, null=True, related_name='booking')
    service = models.ForeignKey('therapists.TherapistService', on_delete=models.SET_NULL, null=True, related_name='booking')
    number_of_customers = models.PositiveIntegerField(default=1)  # Directly store the number of customers as an integer
    address = models.CharField(max_length=255)
    booking_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    prices = models.JSONField(default=list)

    def __str__(self):
        formatted_date_time = self.booking_date_time.strftime("%Y-%m-%d %H:%M")
        return (
            f'Booking ID: {self.id}\n'
            f'Customer: {self.customer.user.username}\n'
            f'Therapist: {self.therapist.user.username}\n'
            f'Booking Time: {formatted_date_time}\n'
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

    def __str__(self):
        return self.name

    def get_price(self, duration, customer_type):
        """
        Retrieve the price for a given duration and customer type.

        :param duration: str, e.g., "60", "90", "120"
        :param customer_type: str, e.g., "single", "couple", "group"
        :return: decimal.Decimal or None if not found
        """
        for entry in self.service_lengths:
            if str(entry[0]) == duration:  # Match the duration
                return entry[1].get(customer_type)  # Return the price for the specified customer type
        return None  # Return None if no matching duration or customer type is found