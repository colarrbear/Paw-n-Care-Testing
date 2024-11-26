"""URLs for the moneymap app."""

from django.urls import path
from . import views

app_name = "paw_n_care"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    path('home/pet/', views.PetHome.as_view(), name='pet-home'),
    path('home/owner/', views.OwnerHome.as_view(), name='owner-home'),
    path('home/medical-record/', views.MedRecHome.as_view(), name='medical-record-home'),
    path('home/billing/', views.BillingHome.as_view(), name='billing-home'),
    path('appointments/', views.Appointments.as_view(), name='appointments'),
    path('medical-records/', views.MedRec.as_view(), name='medical-records'),
    path('billing/', views.Bill.as_view(), name='billing'),
    path('statistic/', views.Statistic.as_view(), name='statistic'),
    path('home/edit/appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('home/edit/pet/<pet_id>/', views.edit_pet, name='edit_pet'),
    path('home/edit/owner/<owner_id>/', views.edit_owner, name='edit_owner'),
    path('home/edit/medical-record/<medical_record_id>/', views.edit_medical_record, name='edit_medical_record'),
    path('home/edit/billing/<billing_id>/', views.edit_billing, name='edit_billing'),
]
