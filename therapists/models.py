from django.db import models
from django.contrib.auth import get_user_model
from core.models import AcceptedCustomerGroups  # Import the existing model
from multiselectfield import MultiSelectField



class Therapist(models.Model):
    GENDER_CHOICE = [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('O', 'Other'),
    ]

    CUSTOMER_CHOICES = [
        ('single', 'Single'),
        ('couple', 'Couple'),
        ('group', 'Group'),
    ]

    PRONOUN_CHOICES = [
        ('she/her', 'She/Her'),
        ('he/him', 'He/Him'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    age = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    picture = models.ImageField(upload_to='therapist_pictures/')
    qualifications = models.CharField(max_length=1000, null=True, blank=True)
    specialties = models.CharField(max_length=1000, null=True, blank=True)
    years_xp = models.IntegerField()
    accepted_customer_groups = MultiSelectField(choices=CUSTOMER_CHOICES, blank=True)
    provided_equipment = models.TextField(max_length=1000, blank=True, null=True)
    required_equipment = models.TextField(max_length=1000, blank=True, null=True)
    pronouns = models.CharField(max_length=20, choices=PRONOUN_CHOICES, default='other')

    def __str__(self):
        return self.user.username




class TherapistService(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey('core.Service', on_delete=models.CASCADE, related_name='therapist_services')
    base_price = models.DecimalField(max_digits=6, decimal_places=2, default=60)
    prices = models.JSONField(default=list)

    def __str__(self):
        return f"{self.therapist.first_name} - {self.service.name} (${self.price})"



class Certification(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='certification')
    name = models.CharField(max_length=100, blank=True, null=True)
    issuing_org = models.CharField(max_length=100, blank=True, null=True)
    issuing_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    certif_file = models.FileField(upload_to="uploads/")

    def __str__(self):
        return f"{self.therapist.name} - {self.name}"
