from django.db import models
from django.contrib.auth.models import User
# The user model doesn't need to be defined because it's built in Django
# We import it here to use some of the fields in the Customer model

class Customer(models.Model):

    GENDER_CHOICE =  [
        ('W', 'Woman'),
        ('M', 'Man'),
        ('O', 'Other'),
    ]

    # Import User fields to use them as Customer fields
    # customers will be deleted automatically when the associated user is
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE), null=True
    description = models.CharField(1000), null=True
    picture = models.ImageField(upload_to='customer_pictures/'), null=True
    # We'll use the Pillow library to upload + store images and use the image fields

    def __str__(self):
        return self.user.username

# This overrides the delete method to also delete the associated user
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()