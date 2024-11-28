from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from customers.models import Customer

class CustomerModelTest(TestCase):
    def setUp(self):
        self.fake = Faker()

        # Create fake user
        self.user = User.objects.create_user(username=self.fake.user_name(), email=self.fake.email(), password='password123')

        # Create fake customer
        self.customer = Customer.objects.create(
            user=self.user,
            name=self.fake.name(),
            gender='M',
            description=self.fake.text(),
            picture=None
        )

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)