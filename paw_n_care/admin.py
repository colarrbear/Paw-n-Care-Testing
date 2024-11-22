from django.contrib import admin

# Register your models here.
from .models import Appointment, Owner, Pet, Veterinarian, MedicalRecord

admin.site.register(Appointment)
admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(Veterinarian)
admin.site.register(MedicalRecord)