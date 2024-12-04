from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from therapists.models import Therapist, TherapistService
from customers.models import Customer
from core.models import Service, Booking
from django.utils import timezone

class ModelIntegrationTest(TestCase):
    def setUp(self):
        self.fake = Faker()

        # Create fake users
        self.user1 = User.objects.create_user(username=self.fake.user_name(), email=self.fake.email(), password='password123')
        self.user2 = User.objects.create_user(username=self.fake.user_name(), email=self.fake.email(), password='password123')

        # Create fake customer
        self.customer = Customer.objects.create(
            user=self.user1,
            name=self.fake.name(),
            gender='M',
            description=self.fake.text(),
            picture=None
        )

        # Create fake therapist
        self.therapist = Therapist.objects.create(
            user=self.user2,
            name=self.fake.name(),
            gender='W',
            description=self.fake.text(),
            picture='picture.jpg',
            specialties=self.fake.text(max_nb_chars=1000),
            years_xp=self.fake.random_int(min=1, max=40),
            number_of_customers='one',
            equipment_pref=self.fake.text(max_nb_chars=1000)
        )
        self.therapist.number_of_customers.set([self.customer_number_one, self.customer_number_couple])

        # Create fake service
        self.service = Service.objects.create(
            name=self.fake.word(),
            description=self.fake.text(),
            base_price=self.fake.pydecimal(left_digits=4, right_digits=2, positive=True),
            picture=None
        )

        # Create fake therapist service
        self.therapist_service = TherapistService.objects.create(
            therapist=self.therapist,
            service=self.service,
            price=self.fake.pydecimal(left_digits=4, right_digits=2, positive=True)
        )

        # Create fake booking
        self.booking = Booking.objects.create(
            therapist=self.therapist,
            customer=self.customer,
            service=self.therapist_service,
            number_of_customers='one',
            booking_date_time=timezone.now(),
            created_at=timezone.now()
        )

    def test_models_integration(self):
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Therapist.objects.count(), 1)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(TherapistService.objects.count(), 1)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(self.booking.customer.user.username, self.customer.user.username)
        self.assertEqual(self.booking.therapist.user.username, self.therapist.user.username)
        self.assertEqual(self.booking.service.service.name, self.service.name)

    def test_therapist_fields(self):
        therapist = Therapist.objects.get(id=self.therapist.id)
        self.assertEqual(therapist.specialties, self.therapist.specialties)
        self.assertEqual(therapist.years_xp, self.therapist.years_xp)
        self.assertEqual(therapist.number_of_customers, self.therapist.number_of_customers)
        self.assertEqual(therapist.equipment_pref, self.therapist.equipment_pref)
        
    def test_number_of_customers(self):
        therapist = Therapist.objects.get(id=self.therapist.id)
        customer_numbers = therapist.number_of_customers.all()
        self.assertEqual(customer_numbers.count(), 2)
        self.assertIn(self.customer_number_one, customer_numbers)
        self.assertIn(self.customer_number_couple, customer_numbers)