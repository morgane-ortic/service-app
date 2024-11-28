from django.db import models
from django.contrib.auth.models import User

class Therapist(models.Model):
    GENDER_CHOICE = [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    picture = models.ImageField(upload_to='therapist_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class TherapistService(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='therapist_services')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.therapist.name} - {self.service.name} (${self.price})"
