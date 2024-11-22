from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


# Create your views here.
class Appointments(TemplateView):
    template_name = 'appointments.html'

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
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        owner_first_name = request.POST.get('owner_first_name')
        owner_last_name = request.POST.get('owner_last_name')
        owner_email = request.POST.get('owner_email')
        owner_phone = request.POST.get('owner_phone')

        # Here you can process or save the data as necessary

        # After processing the form, redirect to the same page
        return HttpResponseRedirect(request.path_info)


class MedRec(TemplateView):
    template_name = 'medical-records.html'


class Billing(TemplateView):
    template_name = 'billing.html'


class Statistic(TemplateView):
    template_name = 'statistic.html'
