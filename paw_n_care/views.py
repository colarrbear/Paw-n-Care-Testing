from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from paw_n_care.models import Appointment, Owner, Pet, Veterinarian, MedicalRecord, Billing


# Create your views here.
class Appointments(TemplateView):
    template_name = 'appointments.html'

    def get(self, request, *args, **kwargs):
        # Assuming you're fetching the appointments here
        # call all vet ids
        vet = Veterinarian.objects.all()

        return render(request, self.template_name, {'vets': vet})

    def post(self, request, *args, **kwargs):
        # Assuming you're handling the form data here
        reason = request.POST.get('reason')
        status = request.POST.get('status')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        pet_name = request.POST.get('pet_name')
        species = request.POST.get('species')
        breed = request.POST.get('breed')
        weight = request.POST.get('weight')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        owner_first_name = request.POST.get('owner_first_name')
        owner_last_name = request.POST.get('owner_last_name')
        owner_email = request.POST.get('owner_email')
        owner_phone = request.POST.get('owner_phone')
        address = request.POST.get('address')
        vet_id = request.POST.get('vet_id')

        # Here you can process or save the data as necessary
        try:
            owner = Owner.objects.create(
                first_name=owner_first_name,
                last_name=owner_last_name,
                address=address,
                phone_number=owner_phone,
                email=owner_email,
                registration_date=timezone.now()
            )
            owner.save()

            pet = Pet.objects.create(
                owner=owner,
                name=pet_name,
                species=species,
                breed=breed,
                date_of_birth=date_of_birth,
                gender=gender,
                weight=weight
            )
            pet.save()

            appointment = Appointment.objects.create(
                pet=pet,
                owner=owner,
                vet=Veterinarian.objects.get(vet_id=vet_id),
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status=status
            )
            appointment.save()

        except Exception as e:
            # Handle the error as needed
            print(f"Error saving appointment: {e}")

        # After processing the form, redirect to the same page
        return redirect('paw_n_care:appointments')


class MedRec(TemplateView):
    template_name = 'medical-records.html'

    def get(self, request, *args, **kwargs):
        # Fetch all necessary data for the medical records page
        pets = Pet.objects.all()
        vets = Veterinarian.objects.all()
        
        context = {
            'pets': pets,
            'vets': vets
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            # Extract form data
            appointment_id = request.POST.get('appointment_id')
            visit_date = request.POST.get('visit_date')
            diagnosis = request.POST.get('diagnosis')
            treatment = request.POST.get('treatment')
            prescribed_medication = request.POST.get('prescribed_medication')
            notes = request.POST.get('notes', '')

            # Fetch the appointment related to the appointment_id
            appointment = Appointment.objects.get(pk=appointment_id)

            # Get the related pet and vet from the appointment
            pet = appointment.pet
            vet = appointment.vet

            # Create medical record
            medrec = MedicalRecord.objects.create(
                pet=pet,
                vet=vet,
                visit_date=visit_date,
                diagnosis=diagnosis,
                treatment=treatment,
                prescribed_medication=prescribed_medication,
                notes=notes
            )
            medrec.save()

        except Exception as e:
            # Handle the error as needed
            print(f"Error saving medical-records: {e}")

        # After processing the form, redirect to the same page
        return redirect('paw_n_care:medical-records')


class Billing(TemplateView):
    # Appointment, Owner, Pet, Veterinarian, MedicalRecord, Billing
    template_name = 'billing.html'
    def get(self, request, *args, **kwargs):
        # Fetch all appointments for the user to select one for billing
        appointments = Appointment.objects.all()  # Or filter appointments as per your requirements

        context = {
            'appointments': appointments
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        try:
            # Extract form data
            appointment_id = request.POST.get('appointment_id')
            total_amount = request.POST.get('total_amount')
            payment_status = request.POST.get('payment_status')
            payment_method = request.POST.get('payment_method')
            payment_date = request.POST.get('payment_date')

            # Fetch the appointment related to the appointment_id
            appointment = Appointment.objects.get(pk=appointment_id)

            # Get the related pet and vet from the appointment
            pet = appointment.pet
            vet = appointment.vet

            # Create medical record
            billing = Billing.objects.create(
                appointment=appointment,
                total_amount=total_amount,
                payment_status=payment_status,
                payment_method=payment_method,
                payment_date=payment_date
            )
            billing.save()

        except Exception as e:
            # Handle the error as needed
            print(f"Error saving billing: {e}")

        # After processing the form, redirect to the same page
        return redirect('paw_n_care:billing')


class Statistic(TemplateView):
    template_name = 'statistic.html'
