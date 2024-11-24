"""URLs for the moneymap app."""

from django.urls import path
from . import views

app_name = "paw_n_care"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
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
]
