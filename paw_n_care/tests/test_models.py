from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Owner, Pet, Veterinarian, Appointment, MedicalRecord, Billing
from datetime import datetime, timedelta
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.utils import timezone


class OwnerModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )


        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Pet St",
            phone_number="1234567890",
            email="john@example.com",
            registration_date=timezone.now()
        )

    def test_owner_creation(self):
        self.assertEqual(self.owner.first_name, "John")
        self.assertEqual(self.owner.last_name, "Doe")
        self.assertEqual(self.owner.email, "john@example.com")
        self.assertTrue(isinstance(self.owner, Owner))
        self.assertEqual(str(self.owner), "John Doe")

    def test_phone_number_validation(self):
        self.owner.phone_number = "1234567890123456"
        with self.assertRaises(ValidationError):
            self.owner.full_clean()

    def test_view_owner_data(self):
        """Test TC05: View owner data"""
        self.client.login(username='testuser', password='testpass123')

        self.assertEqual(Owner.objects.count(), 1)
        owner = Owner.objects.first()
        print(f"Owner in database: {owner}")

        response = self.client.get(reverse('paw_n_care:owner-home'))
        self.assertEqual(response.status_code, 200)

        if hasattr(response, 'context'):
            print("Context data:", response.context)
        else:
            print("No context data available in response")

        print(response.content.decode())

        self.assertContains(response, str(owner.owner_id))
        self.assertContains(response, owner.first_name)
        self.assertContains(response, owner.last_name)

class PetModelTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Pet St",
            phone_number="1234567890",
            email="john@example.com",
            registration_date=datetime.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner,
            name="Fluffy",
            species="Cat",
            breed="Persian",
            date_of_birth=datetime.now() - timedelta(days=365*3),
            gender="Female",
            weight=4.5
        )

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, "Fluffy")
        self.assertEqual(self.pet.species, "Cat")
        self.assertEqual(self.pet.owner.first_name, "John")
        self.assertEqual(str(self.pet), "Fluffy (1)")