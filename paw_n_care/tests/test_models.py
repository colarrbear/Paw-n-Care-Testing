from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Owner, Pet, Veterinarian, Appointment, MedicalRecord, Billing
from datetime import datetime, timedelta
from django.urls import reverse
from django.test import Client
from datetime import datetime, timedelta, time
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
        """Validate that phone numbers respect max_length constraint (10 digits)."""

        # Valid phone number (10 digits) should not raise an error
        self.owner.phone_number = "1234567890"
        try:
            self.owner.full_clean()
        except ValidationError:
            self.fail("Valid phone number raised ValidationError")

        # Invalid phone number (11 digits) should raise ValidationError
        self.owner.phone_number = "12345678901"
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

    def test_pet_creation_with_negative_weight(self):
        """Pet creation should raise ValidationError if weight is negative."""
        pet = Pet(
            owner=self.owner,
            name="Ghost",
            species="Dog",
            breed="Husky",
            date_of_birth=datetime.now() - timedelta(days=365),
            gender="Male",
            weight=-2.0
        )
        with self.assertRaises(ValidationError):
            pet.full_clean()
            pet.save()

class AppointmentModelTest(TestCase):
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
        self.vet = Veterinarian.objects.create(
            first_name="Jane",
            last_name="Smith",
            specialization="Feline",
            license_number="VET123",
            phone_number="0987654321",
            email="jane@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.owner,
            vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Annual checkup",
            status="Scheduled"
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.reason, "Annual checkup")
        self.assertEqual(self.appointment.vet.full_name, "Jane Smith")
        self.assertEqual(str(self.appointment), "Appointment 1 for Fluffy")

class MedicalRecordModelTest(TestCase):
    def setUp(self):
        # Create all related objects first
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
        self.vet = Veterinarian.objects.create(
            first_name="Jane",
            last_name="Smith",
            specialization="Feline",
            license_number="VET123",
            phone_number="0987654321",
            email="jane@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.owner,
            vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Annual checkup",
            status="Scheduled"
        )
        self.record = MedicalRecord.objects.create(
            appointment=self.appointment,
            pet=self.pet,
            vet=self.vet,
            visit_date=datetime.now(),
            diagnosis="Healthy",
            treatment="Vaccination",
            prescribed_medication="None",
            notes="Good health"
        )

    def test_medical_record_creation(self):
        self.assertEqual(self.record.diagnosis, "Healthy")
        self.assertEqual(self.record.treatment, "Vaccination")
        self.assertEqual(str(self.record), "Record 1 for Fluffy")

class BillingModelTest(TestCase):
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
        self.vet = Veterinarian.objects.create(
            first_name="Jane",
            last_name="Smith",
            specialization="Feline",
            license_number="VET123",
            phone_number="0987654321",
            email="jane@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.owner,
            vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Annual checkup",
            status="Scheduled"
        )
        self.billing = Billing.objects.create(
            appointment=self.appointment,
            total_amount=100.00,
            payment_status="Paid",
            payment_method="Credit Card",
            payment_date=datetime.now()
        )

    def test_billing_creation(self):
        self.assertEqual(self.billing.total_amount, 100.00)
        self.assertEqual(self.billing.payment_status, "Paid")
        self.assertEqual(str(self.billing), "Bill 1 for Appointment 1")

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="admin",
                                             password="admin123")

    def test_login_with_correct_info(self):
        response = self.client.post(reverse('paw_n_care:login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertRedirects(response, '/')

    def test_login_with_incorrect_info(self):
        response = self.client.post(reverse('paw_n_care:login'), {
            'username': 'admin',
            'password': 'wrongpass'
        })
        self.assertRedirects(response, reverse('paw_n_care:login'))

class AppointmentStatusUpdateTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Alex", last_name="Lee", address="XYZ Road",
            phone_number="5555555555", email="alex@example.com",
            registration_date=datetime.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner, name="Bobby", species="Dog", breed="Beagle",
            date_of_birth=datetime.now() - timedelta(days=365),
            gender="Male", weight=15.2
        )
        self.vet = Veterinarian.objects.create(
            first_name="Sara", last_name="Connor", specialization="Canine",
            license_number="VET999", phone_number="2222222222", email="sara@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet, owner=self.owner, vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Routine Check", status="Scheduled"
        )

    def test_update_appointment_status(self):
        self.appointment.status = "Completed"
        self.appointment.save()
        updated = Appointment.objects.get(pk=self.appointment.pk)
        self.assertEqual(updated.status, "Completed")

    def test_view_appointment_list(self):
        response = self.client.get(reverse('paw_n_care:appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bobby")


class AppointmentOverlapTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Alex", last_name="Lee", address="XYZ Road",
            phone_number="5555555555", email="alex@example.com",
            registration_date=datetime.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner, name="Bobby", species="Dog", breed="Beagle",
            date_of_birth=datetime.now() - timedelta(days=365),
            gender="Male", weight=15.2
        )
        self.vet = Veterinarian.objects.create(
            first_name="Sara", last_name="Connor", specialization="Canine",
            license_number="VET999", phone_number="2222222222",
            email="sara@example.com"
        )

        # Create first appointment from 10:00 to 10:30
        self.appointment_time = time(10, 0)
        self.appointment1 = Appointment.objects.create(
            pet=self.pet, owner=self.owner, vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=self.appointment_time,
            reason="Checkup", status="Scheduled"
        )

    def test_overlapping_appointments(self):
        # Create second appointment 15 minutes before first appointment ends (assuming 30 min duration)
        overlapping_time = (datetime.combine(datetime.now().date(),
                                             self.appointment_time) +
                            timedelta(minutes=15)).time()

        # This should raise an exception or fail validation
        with self.assertRaises(Exception):
            Appointment.objects.create(
                pet=self.pet, owner=self.owner, vet=self.vet,
                appointment_date=datetime.now().date(),
                appointment_time=overlapping_time,
                reason="Emergency", status="Scheduled"
            )

class MedicalRecordViewTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Alex", last_name="Lee", address="XYZ Road",
            phone_number="5555555555", email="alex@example.com",
            registration_date=datetime.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner, name="Bobby", species="Dog", breed="Beagle",
            date_of_birth=datetime.now() - timedelta(days=365),
            gender="Male", weight=15.2
        )
        self.vet = Veterinarian.objects.create(
            first_name="Sara", last_name="Connor", specialization="Canine",
            license_number="VET999", phone_number="2222222222", email="sara@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet, owner=self.owner, vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Routine Check", status="Completed"
        )
        self.medical_record = MedicalRecord.objects.create(
            appointment=self.appointment,
            pet=self.pet,
            vet=self.vet,
            visit_date=datetime.now(),
            diagnosis="Allergy",
            treatment="Antihistamine",
            prescribed_medication="Cetirizine",
            notes="Monitor"
        )

    def test_view_medical_record_details(self):
        user = User.objects.create_user(username="testuser",
                                        password="password")
        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse('paw_n_care:medical-records'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Medical Records")

        record = MedicalRecord.objects.filter(diagnosis="Allergy").first()
        self.assertIsNotNone(record)
        self.assertEqual(record.diagnosis, "Allergy")

class BillingUpdateTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="Alex", last_name="Lee", address="XYZ Road",
            phone_number="5555555555", email="alex@example.com",
            registration_date=datetime.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner, name="Bobby", species="Dog", breed="Beagle",
            date_of_birth=datetime.now() - timedelta(days=365),
            gender="Male", weight=15.2
        )
        self.vet = Veterinarian.objects.create(
            first_name="Sara", last_name="Connor", specialization="Canine",
            license_number="VET999", phone_number="2222222222", email="sara@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet, owner=self.owner, vet=self.vet,
            appointment_date=datetime.now().date(),
            appointment_time=datetime.now().time(),
            reason="Routine Check", status="Completed"
        )
        self.billing = Billing.objects.create(
            appointment=self.appointment,
            total_amount=150.00,
            payment_status="Pending",
            payment_method="Cash",
            payment_date=datetime.now()
        )

    def test_update_payment_status(self):
        self.billing.payment_status = "Paid"
        self.billing.save()
        updated = Billing.objects.get(pk=self.billing.pk)
        self.assertEqual(updated.payment_status, "Paid")

    def test_view_billing_list(self):
        user = User.objects.create_user(username="testuser",
                                        password="password")
        self.client.login(username="testuser", password="password")

        response = self.client.get(reverse('paw_n_care:billing'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Billing")

        billing = Billing.objects.filter(total_amount=150.00).first()
        self.assertIsNotNone(billing)
        self.assertEqual(billing.total_amount, 150.00)

class StatisticPageTest(TestCase):
    def setUp(self):
        self.vet = Veterinarian.objects.create(
            first_name="Eva", last_name="Jones", specialization="Exotic",
            license_number="VET321", phone_number="1111222233", email="eva@example.com"
        )

    def test_view_statistic_page(self):
        response = self.client.get(reverse('paw_n_care:statistic'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Statistic")

class OwnerUpdateTest(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890",
            registration_date=datetime.now()
        )

    def test_owner_update(self):
        self.owner.first_name = "Jonathan"
        self.owner.save()
        updated = Owner.objects.get(pk=self.owner.pk)
        self.assertEqual(updated.first_name, "Jonathan")

class VeterinarianStatisticsTest(TestCase):
    def setUp(self):
        self.vet = Veterinarian.objects.create(
            first_name="Sarah",
            last_name="Johnson",
            specialization="Canine",
            license_number="VET456",
            phone_number="1234567890",
            email="sarah@example.com"
        )

    def test_statistic_page_includes_vets(self):
        response = self.client.get(reverse('paw_n_care:statistic'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Statistic")

        self.assertIn('vets', response.context)
        self.assertEqual(response.context['vets'].count(), 1)


class MedicalRecordUpdateTest(TestCase):
    """Test Case ID: TC10 - Update medical record"""

    def setUp(self):
        # Create necessary related objects
        self.owner = Owner.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Pet St",
            phone_number="1234567890",
            email="john@example.com",
            registration_date=timezone.now()
        )
        self.pet = Pet.objects.create(
            owner=self.owner,
            name="Fluffy",
            species="Cat",
            breed="Persian",
            date_of_birth=timezone.now() - timedelta(days=365 * 3),
            gender="Female",
            weight=4.5
        )
        self.vet = Veterinarian.objects.create(
            first_name="Jane",
            last_name="Smith",
            specialization="Feline",
            license_number="VET123",
            phone_number="0987654321",
            email="jane@example.com"
        )
        self.appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.owner,
            vet=self.vet,
            appointment_date=timezone.now().date(),
            appointment_time=timezone.now().time(),
            reason="Annual checkup",
            status="Completed"
        )
        self.medical_record = MedicalRecord.objects.create(
            appointment=self.appointment,
            pet=self.pet,
            vet=self.vet,
            visit_date=timezone.now(),
            diagnosis="Healthy",
            treatment="Vaccination",
            prescribed_medication="None",
            notes="Initial checkup completed"
        )

        # Create test user
        self.user = User.objects.create_user(
            username='vetuser',
            password='vetpass123'
        )
        self.client = Client()

    def test_update_medical_record(self):
        """Verify that existing medical records can be updated"""
        # Log in the user (simulating vet privileges)
        self.client.login(username='vetuser', password='vetpass123')

        # Original values
        original_treatment = self.medical_record.treatment
        original_notes = self.medical_record.notes

        # New test data to update
        updated_treatment = "Vaccination and deworming"
        updated_notes = "Pet responded well to treatment. Needs follow-up in 6 months."

        # Update the medical record
        self.medical_record.treatment = updated_treatment
        self.medical_record.notes = updated_notes
        self.medical_record.save()

        # Retrieve the updated record from database
        updated_record = MedicalRecord.objects.get(pk=self.medical_record.pk)

        # Verify the record was updated
        self.assertEqual(updated_record.treatment, updated_treatment)
        self.assertEqual(updated_record.notes, updated_notes)
        self.assertNotEqual(updated_record.treatment, original_treatment)
        self.assertNotEqual(updated_record.notes, original_notes)

        # Verify the original diagnosis and other fields remain unchanged
        self.assertEqual(updated_record.diagnosis, "Healthy")
        self.assertEqual(updated_record.prescribed_medication, "None")
        self.assertEqual(updated_record.pet, self.pet)
        self.assertEqual(updated_record.vet, self.vet)