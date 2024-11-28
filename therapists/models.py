from django.db import models
from django.contrib.auth import get_user_model

class Therapist(models.Model):
    GENDER_CHOICE = [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    picture = models.ImageField(upload_to='therapist_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class TherapistService(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, related_name='therapist_services')
    # Using a string reference for core.Service instead of direct import to avoid circular imports
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.therapist.name} - {self.service.name} (${self.price})"
