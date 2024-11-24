from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.db.models import Count, Sum, Avg

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
            species=species,
            breed=data.get('breed'),
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
        # Get all veterinarians for the dropdown
        veterinarians = Veterinarian.objects.all().values('vet_id', 'first_name', 'last_name')

        # Get the selected veterinarian ID from the request (default to the first vet)
        selected_vet_id = request.GET.get('vet', veterinarians[0]['vet_id'] if veterinarians else None)

        # "Individual statistics for the selected veterinarian"
        # Get statistics for the selected veterinarian
        appointments = Appointment.objects.filter(vet_id=selected_vet_id).count()
        pets_managed = Pet.objects.filter(appointments__vet_id=selected_vet_id).distinct().count()
        bills_paid = Billing.objects.filter(appointment__vet_id=selected_vet_id).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Get total statistics for all veterinarians
        total_appointments = Appointment.objects.count()
        total_pets_managed = Pet.objects.distinct().count()
        total_bills_paid = Billing.objects.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Calculate percentage for each statistic
        appointment_percentage = (appointments / total_appointments * 100) if total_appointments else 0
        pets_managed_percentage = (pets_managed / total_pets_managed * 100) if total_pets_managed else 0
        bills_paid_percentage = (bills_paid / total_bills_paid * 100) if total_bills_paid else 0

        # "Clinic-wide statistics"
        # Calculate average appointments per month
        current_month = timezone.now().month
        current_year = timezone.now().year
        monthly_appointments = Appointment.objects.filter(
            appointment_date__month=current_month,
            appointment_date__year=current_year
        ).count()

        # Calculate unique returning owners in the last 6 months
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        returning_owners = Owner.objects.filter(
            pets__appointments__appointment_date__gte=six_months_ago
        ).distinct().count()

        # Get most frequent species
        most_frequent_species = Pet.objects.values('species')\
            .annotate(count=Count('pet_id'))\
            .order_by('-count')

        if len(most_frequent_species) > 1 and most_frequent_species[0]['count'] == most_frequent_species[1]['count']:
            most_frequent_species = {'species': 'N/A', 'count': 0}
        else:
            most_frequent_species = most_frequent_species.first()
        
        # Calculate percentage of appointments resulting in medications
        appointments_with_meds = Appointment.objects.filter(
            pet__medical_records__prescribed_medication__isnull=False
        ).distinct().count()

        # Calculate percentage
        medication_percentage = (appointments_with_meds / total_appointments * 100) if total_appointments else 0

        # Calculate Pet Average Weight Statistics for Dogs, Cats, and Other
        dog_avg_weight = Pet.objects.filter(species='Dog').aggregate(avg_weight=Avg('weight'))['avg_weight'] or 0
        cat_avg_weight = Pet.objects.filter(species='Cat').aggregate(avg_weight=Avg('weight'))['avg_weight'] or 0
        other_avg_weight = Pet.objects.exclude(species__in=['Dog', 'Cat']).aggregate(avg_weight=Avg('weight'))['avg_weight'] or 0

        # "Appointment Statistics"
        # Top Vet by Completed Appointments
        completed_appointments = Appointment.objects.filter(status='Completed')
        top_vets = completed_appointments.values('vet_id')\
            .annotate(completed_count=Count('appointment_id'))\
            .order_by('-completed_count')[:1]

        top_vet_full_name = ''
        if top_vets:
            vet_detail = Veterinarian.objects.get(vet_id=top_vets[0]['vet_id'])
            top_vet_full_name = vet_detail.full_name

        # Appointment Status Distribution in the past year
        scheduled_count = Appointment.objects.filter(status='Scheduled', appointment_date__gte=timezone.now()-timezone.timedelta(days=365)).count()
        completed_count = Appointment.objects.filter(status='Completed', appointment_date__gte=timezone.now()-timezone.timedelta(days=365)).count()
        canceled_count = Appointment.objects.filter(status='Canceled', appointment_date__gte=timezone.now()-timezone.timedelta(days=365)).count()

        # "Billing & Payment Analysis"
        # Average billing amount
        avg_billing_amount = Billing.objects.aggregate(Avg('total_amount'))['total_amount__avg'] or 0
        
        # Sum Billing this month
        sum_billing_this_month = Billing.objects.filter(payment_date__month=current_month, payment_date__year=current_year).aggregate(total=Sum('total_amount'))['total'] or 0

        # Invoice Status Overview
        paid_count = Billing.objects.filter(payment_status='Paid').count()
        pending_count = Billing.objects.filter(payment_status='Pending').count()
        overdue_count = Billing.objects.filter(payment_status='Overdue').count()
        total_invoices = Billing.objects.count()
        # Calculate percentages
        paid_percentage = (paid_count / total_invoices * 100) if total_invoices else 0
        pending_percentage = (pending_count / total_invoices * 100) if total_invoices else 0
        overdue_percentage = (overdue_count / total_invoices * 100) if total_invoices else 0

        # Payment Methods and Status
        # Calculate the total number of invoices and the count for each payment method
        total_invoices = Billing.objects.count()
        credit_card_count = Billing.objects.filter(payment_method='Credit Card').count()
        cash_count = Billing.objects.filter(payment_method='Cash').count()
        bank_transfer_count = Billing.objects.filter(payment_method='Bank Transfer').count()

        # Calculate the percentages for each payment method (rounded)
        credit_card_percentage = (credit_card_count / total_invoices * 100) if total_invoices else 0
        cash_percentage = (cash_count / total_invoices * 100) if total_invoices else 0
        bank_transfer_percentage = (bank_transfer_count / total_invoices * 100) if total_invoices else 0

        # Return the data to the template, including the selected vet ID
        return render(request, self.template_name, {
            'vets': veterinarians,
            'selected_vet_id': selected_vet_id,

            # Individual vet statistics
            'appointments': appointments,
            'pets_managed': pets_managed,
            'bills_paid': bills_paid,
            'appointment_percentage': round(appointment_percentage),
            'pets_managed_percentage': round(pets_managed_percentage),
            'bills_paid_percentage': round(bills_paid_percentage),

            # Clinic-wide statistics
            'avg_monthly_appointments': monthly_appointments,
            'returning_owners': returning_owners,
            'most_frequent_species': most_frequent_species['species'] if most_frequent_species else 'N/A',
            'medication_percentage': round(medication_percentage),

            # Pet Average Weight Statistics
            'dog_avg_weight': dog_avg_weight,
            'cat_avg_weight': cat_avg_weight,
            'other_avg_weight': other_avg_weight,

            # Appointment Statistics
            'top_vets': top_vet_full_name,
            'scheduled_count': scheduled_count,
            'completed_count': completed_count,
            'canceled_count': canceled_count,

            # Billing & Payment Analysis
            'avg_billing_amount': avg_billing_amount,
            'sum_billing_this_month': sum_billing_this_month,
            'paid_percentage': round(paid_percentage),
            'pending_percentage': round(pending_percentage),
            'overdue_percentage': round(overdue_percentage),
            'total_invoices': total_invoices,
            # Invoice Status Overview
            'credit_card_percentage': round(credit_card_percentage),
            'cash_percentage': round(cash_percentage),
            'bank_transfer_percentage': round(bank_transfer_percentage),
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

def redirect_to_login(request):
    # Redirect to the login page
    return HttpResponseRedirect('/login/')
