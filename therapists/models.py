from django.db import models
from django.contrib.auth import get_user_model


class Therapist(models.Model):
    GENDER_CHOICE = [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('O', 'Other'),
    ]

    CUSTOMER_NUMBER = [
        ('one', 'One'),
        ('couple', 'Couple'),
        ('group', 'Group'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    description = models.TextField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    picture = models.ImageField(upload_to='therapist_pictures/')
    # Use Pillow library in views for images? For resizing/cropping
    qualifications = models.CharField(max_length=1000, null=True, blank=True)
    specialties = models.CharField(max_length=1000, null=True, blank=True)
    years_xp = models.IntegerField()
    equipment_pref = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.username

class TherapistService(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, related_name='therapist_services')
    # Using a string reference for core.Service instead of direct import to avoid circular imports
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.therapist.name} - {self.service.name} (${self.price})"


class Certification(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='certification')
    name = models.CharField(max_length=100, blank=True, null=True)
    issuing_org = models.CharField(max_length=100, blank=True, null=True)
    issuing_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    certif_file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"{self.therapist.name} - {self.certification.name}"