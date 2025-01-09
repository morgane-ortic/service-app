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
            picture='customer_pictures/picture.jpg'
        )

    def test_customer_creation(self):
        self.assertEqual(Customer.objects.count(), 1)

    def test_customer_fields(self):
        customer = Customer.objects.get(id=self.customer.id)
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.name, self.customer.name)
        self.assertEqual(customer.gender, self.customer.gender)
        self.assertEqual(customer.description, self.customer.description)
        self.assertEqual(customer.picture, self.customer.picture)

    def test_customer_str(self):
        customer = Customer.objects.get(id=self.customer.id)
        self.assertEqual(str(customer), self.user.username)

    def test_customer_delete(self):
        customer_id = self.customer.id
        user_id = self.user.id
        self.customer.delete()
        self.assertFalse(Customer.objects.filter(id=customer_id).exists())
        self.assertFalse(User.objects.filter(id=user_id).exists())