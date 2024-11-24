from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
# from django.contrib.auth import authenticate, login


from paw_n_care.models import Appointment, Owner, Pet, Veterinarian, MedicalRecord, Billing, User


# Create your views here.
class Appointments(TemplateView):
    template_name = 'appointments.html'

    def get(self, request, *args, **kwargs):
        pets = Pet.objects.all().values('pet_id', 'name', 'species', 'owner__first_name', 'owner__last_name')
        vets = Veterinarian.objects.all().values('vet_id', 'first_name', 'last_name')
        owners = Owner.objects.all().values('owner_id', 'first_name', 'last_name')
        return render(request, self.template_name, {'vets': vets, 'pets': pets, 'owners': owners})

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST

            appointment_date = data.get('appointment_date')
            appointment_time = data.get('appointment_time')
            reason = data.get('reason')
            status = data.get('status')
            vet_id = data.get('vet')

            pet_id = data.get('existing_pet')
            if pet_id:
                self.create_appointment_for_existing_pet(pet_id, vet_id, appointment_date, appointment_time, reason,
                                                         status)
            else:
                self.create_new_pet_and_appointment(data, vet_id, appointment_date, appointment_time, reason, status)

        except Exception as e:
            # Handle the error as needed
            print(f"Error saving appointment: {e}")

        return redirect('paw_n_care:appointments')

    @staticmethod
    def create_appointment_for_existing_pet(pet_id, vet_id, appointment_date, appointment_time, reason, status):
        """Handle appointment creation for an existing pet."""
        pet = Pet.objects.get(pet_id=pet_id)
        owner = pet.owner
        vet = Veterinarian.objects.get(vet_id=vet_id)

        # Create and save the appointment
        Appointment.objects.create(
            pet=pet,
            owner=owner,
            vet=vet,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status=status
        )

    @staticmethod
    def create_new_pet_and_appointment(data, vet_id, appointment_date, appointment_time, reason, status):
        """Handle the creation of a new owner, pet, and their appointment."""
        owner_id = data.get('existing_owner')
        if owner_id:
            owner = Owner.objects.get(owner_id=owner_id)
        else:
            owner = Appointments.create_owner(data)

        pet = Appointments.create_pet(data, owner)
        vet = Veterinarian.objects.get(vet_id=vet_id)

        # Create and save the appointment
        Appointment.objects.create(
            pet=pet,
            owner=owner,
            vet=vet,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status=status
        )

    @staticmethod
    def create_owner(data):
        """Create a new owner."""
        return Owner.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone_number=data.get('phone'),
            email=data.get('email'),
            registration_date=timezone.now()
        )

    @staticmethod
    def create_pet(data, owner):
        """Create a new pet."""
        species = data.get('species').lower()
        if species == 'other':
            species = data.get('new_species').lower()

        return Pet.objects.create(
            owner=owner,
            name=data.get('pet_name'),
            species=species.lower(),
            breed=data.get('breed').lower(),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            weight=data.get('weight')
        )


class MedRec(TemplateView):
    template_name = 'medical-records.html'

    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.all().values('appointment_id', 'pet__name', 'vet__first_name',
                                                        'vet__last_name')

        context = {
            'appointments': appointments
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
                appointment=appointment,
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


class Bill(TemplateView):
    # Appointment, Owner, Pet, Veterinarian, MedicalRecord, Billing
    template_name = 'billing.html'

    def get(self, request, *args, **kwargs):
        # Fetch all appointments for the user to select one for billing
        appointments = Appointment.objects.all().values('appointment_id', 'pet__name', 'vet__first_name',
                                                        'vet__last_name')

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
            bill = Billing.objects.create(
                appointment=appointment,
                total_amount=total_amount,
                payment_status=payment_status,
                payment_method=payment_method,
                payment_date=payment_date
            )
            bill.save()

        except Exception as e:
            # Handle the error as needed
            print(f"Error saving billing: {e}")

        # After processing the form, redirect to the same page
        return redirect('paw_n_care:billing')


class Statistic(TemplateView):
    template_name = 'statistic.html'

    def get(self, request, *args, **kwargs):
        vet = Veterinarian.objects.all().values('vet_id', 'first_name', 'last_name')

        return render(request, self.template_name, {
            'vets': vet,
        })


class Login(TemplateView):
    template_name = 'login.html'

    # Get all users and must check that the input username and password are user's that in database
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            data = request.POST
            username = data.get('username')
            password = data.get('password')
            user = User.objects.get(username=username, password=password)
            if user:
                return redirect('paw_n_care:appointments')
        except Exception as e:
            print(f"Error login: {e}")
        return redirect('paw_n_care:login')


class Logout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('paw_n_care:login')


class Home(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.all().values(
            'appointment_id', 'reason', 'status',
            'appointment_date', 'appointment_time', 'vet__first_name',
            'pet__pet_id', 'pet__name', 'pet__owner__owner_id', 'pet__owner__first_name',
        )

        context = {
            'appointments': appointments,
        }
        return render(request, self.template_name, context)


class MedRecHome(TemplateView):
    template_name = 'home/medical-record-home.html'

    def get(self, request, *args, **kwargs):
        medical_records = MedicalRecord.objects.select_related(
            'appointment',
            'pet',
            'vet'
        ).values(
            'record_id',
            'appointment__appointment_id',
            'pet__name',
            'pet__pet_id',
            'vet__first_name',
            'vet__last_name',
            'visit_date',
            'diagnosis',
            'treatment',
            'prescribed_medication'
        )

        context = {
            'medical_records': medical_records,
        }
        return render(request, self.template_name, context)


class BillingHome(TemplateView):
    template_name = 'home/billing-home.html'

    def get(self, request, *args, **kwargs):
        bills = Billing.objects.select_related(
            'appointment',
            'appointment__pet',
            'appointment__vet'
        ).values(
            'bill_id',
            'appointment__appointment_id',
            'appointment__owner__owner_id',
            'appointment__owner__first_name',
            'appointment__owner__last_name',
            'appointment__pet__name',
            'appointment__pet_id',
            'total_amount',
            'payment_status',
            'payment_method',
            'payment_date'
        )

        context = {
            'bills': bills,
        }

        return render(request, self.template_name, context)


class PetHome(TemplateView):
    template_name = 'home/pet-home.html'

    def get(self, request, *args, **kwargs):
        pets = Pet.objects.all().values('pet_id', 'name', 'species', 'breed', 'date_of_birth', 'gender', 'pet_id',
                                        'weight', 'owner__owner_id', 'owner__first_name')

        context = {
            'pets': pets
        }

        return render(request, self.template_name, context)


class OwnerHome(TemplateView):
    template_name = 'home/owner-home.html'

    def get(self, request, *args, **kwargs):
        owners = Owner.objects.prefetch_related('pets').all()

        context = {
            'owners': owners,
        }
        return render(request, self.template_name, context)


def redirect_to_login(request):
    # Redirect to the login page
    return HttpResponseRedirect('/login/')
