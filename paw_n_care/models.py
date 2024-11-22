from django.db import models

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    registration_date = models.DateTimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=255)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Veterinarian(models.Model):
    vet_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} : {self.vet_id}"


class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='appointments')
    vet = models.ForeignKey(Veterinarian, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Appointment {self.appointment_id} for {self.pet.name}"


class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    vet = models.ForeignKey(Veterinarian, on_delete=models.CASCADE, related_name='medical_records')
    visit_date = models.DateTimeField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescribed_medication = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Record {self.record_id} for {self.pet.name}"


class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20)
    payment_date = models.DateTimeField()

    def __str__(self):
        return f"Bill {self.bill_id} for Appointment {self.appointment.appointment_id}"
