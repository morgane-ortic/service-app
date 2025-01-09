from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from therapists.models import Therapist, TherapistService
from customers.models import Customer
from core.models import Service, Booking, NumberOfCustomers
from django.utils import timezone

class BookingModelTest(TestCase):
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
            address=self.fake.address(),
            specialties=self.fake.text(max_nb_chars=1000),
            years_xp=self.fake.random_int(min=1, max=40),
            equipment_pref=self.fake.text(max_nb_chars=1000)
        )

        # Create fake customer numbers
        self.customer_number_one = NumberOfCustomers.objects.create(choice='one')
        self.customer_number_couple = NumberOfCustomers.objects.create(choice='couple')
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
            customer=self.customer,
            therapist=self.therapist,
            service=self.therapist_service,
            address=self.fake.address(),
            booking_date_time=timezone.now(),
            created_at=timezone.now()
        )
        self.booking.number_of_customers.set([self.customer_number_one, self.customer_number_couple])

    def test_booking_creation(self):
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_fields(self):
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.customer, self.customer)
        self.assertEqual(booking.therapist, self.therapist)
        self.assertEqual(booking.service, self.therapist_service)
        self.assertEqual(booking.address, self.booking.address)
        self.assertEqual(booking.booking_date_time, self.booking.booking_date_time)
        self.assertEqual(booking.created_at, self.booking.created_at)

    def test_booking_number_of_customers(self):
        booking = Booking.objects.get(id=self.booking.id)
        customer_numbers = booking.number_of_customers.all()
        self.assertEqual(customer_numbers.count(), 2)
        self.assertIn(self.customer_number_one, customer_numbers)
        self.assertIn(self.customer_number_couple, customer_numbers)

    def test_booking_str(self):
        booking = Booking.objects.get(id=self.booking.id)
        formatted_date_time = booking.booking_date_time.strftime("%Y-%m-%d %H:%M")
        expected_str = (
            f'Booking ID: {booking.id}\n'
            f'Customer: {booking.customer.user.username}\n'
            f'Therapist: {booking.therapist.user.username}\n'
            f'Booking Time: {formatted_date_time}\n'
        )
        self.assertEqual(str(booking), expected_str)