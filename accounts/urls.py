from django.urls import path
from .views import (
    login_redirect,
    patient_dashboard,
    staff_dashboard,
    staff_create_patient,
    staff_add_medication,
)

urlpatterns = [
    path("portal/", login_redirect, name="portal-home"),
    path("dashboard/", patient_dashboard, name="patient-dashboard"),
    path("staff/", staff_dashboard, name="staff-dashboard"),
    path("staff/create-patient/", staff_create_patient, name="staff-create-patient"),
    path("staff/add-medication/", staff_add_medication, name="staff-add-medication"),
]
