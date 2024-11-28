from django.test import TestCase
from django.contrib.auth.models import User
from faker import Faker
from therapists.models import Therapist, TherapistService
from core.models import Service

class TherapistModelTest(TestCase):
    def setUp(self):
        self.fake = Faker()

        # Create fake user
        self.user = User.objects.create_user(username=self.fake.user_name(), email=self.fake.email(), password='password123')

        # Create fake therapist
        self.therapist = Therapist.objects.create(
            user=self.user,
            name=self.fake.name(),
            gender='W',
            description=self.fake.text(),
            picture=None
        )

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

    def test_therapist_creation(self):
        self.assertEqual(Therapist.objects.count(), 1)
        self.assertEqual(TherapistService.objects.count(), 1)