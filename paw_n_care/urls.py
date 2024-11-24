"""URLs for the moneymap app."""

from django.urls import path
from . import views

app_name = "paw_n_care"

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('', views.Appointments.as_view(), name='appointments'),
    path('medical-records/', views.MedRec.as_view(), name='medical-records'),
    path('billing/', views.Bill.as_view(), name='billing'),
    path('statistic/', views.Statistic.as_view(), name='statistic'),
]
