from django.db import models
from therapists.models import Therapist, TherapistService
from customers.models import Customer


class Booking(models.Model):
    CUSTOMER_NUMBER = [
        ('one', 'One'),
        ('couple', 'Couple'),
        ('group', 'Group'),
    ]

    # 'on_delete=models.NULL' makes sure the booking stays in the DB even if the therapist gets deleted
    # 'null=True' ensures this is possible, by allowing the FK to be set to NULL when the related PK gets deleted
    therapist_id = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, related_name='booking')
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='booking')
    service_id = models.ForeignKey(TherapistService, on_delete=models.SET_NULL, null=True, related_name='booking')
    number_of_customers = models.CharField(max_length=50, choices=CUSTOMER_NUMBER)
    booking_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        formatted_date_time = self.booking_date_time.strftime("%Y-%m-%d %H:%M")
        return  (
            f'Booking ID: {self.id}\n'
            f'Customer: {self.customer.user.username}\n'
            f'Therapist: {self.therapist.user.username}\n'
            f'Booking Time: {formatted_date_time}\n'
        )

class Service(models.Model):
    name = models.CharField(50)
    description = models.CharField(1000), null=True
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    # the max price here is 9999.99
    picture = models.ImageField(upload_to='service_pictures/')
    # We'll use the Pillow library to upload + store images and use the image fields

    def __str__(self):
        return self.name