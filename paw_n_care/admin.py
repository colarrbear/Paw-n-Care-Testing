from django.contrib import admin
from .models import Appointment, Owner, Pet, Veterinarian, MedicalRecord, Billing, User


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'first_name', 'last_name', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('pet_id', 'name', 'owner', 'species', 'breed', 'date_of_birth')
    list_filter = ('species', 'breed')
    search_fields = ('name', 'owner__first_name', 'owner__last_name')


@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    list_display = ('vet_id', 'first_name', 'last_name', 'specialization', 'license_number')
    search_fields = ('first_name', 'last_name', 'license_number')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'pet', 'owner', 'vet', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('pet__name', 'owner__first_name', 'owner__last_name')


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'pet', 'vet', 'visit_date', 'diagnosis')
    list_filter = ('visit_date',)
    search_fields = ('pet__name', 'diagnosis', 'treatment')


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'appointment', 'total_amount', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('appointment__pet__name', 'payment_status')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username')
    search_fields = ('username',)
