from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from paw_n_care.models import Appointment, Owner, Pet, Veterinarian


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


class Billing(TemplateView):
    template_name = 'billing.html'


class Statistic(TemplateView):
    template_name = 'statistic.html'
