"""
Accounts Views Module

Purpose: Handles patient dashboard, staff dashboard, login redirect, and user management views.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponseForbidden

from accounts.models import Profile
from meds.models import Medication
from refills.models import RefillRequest

User = get_user_model()


@login_required
def patient_dashboard(request):
    """Render the patient dashboard for patient users only."""
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == Profile.Role.PROVIDER:
        return redirect("provider-dashboard")
    if profile and profile.role == Profile.Role.STAFF:
        return redirect("staff-dashboard")
    medications = Medication.objects.filter(patient=request.user)
    refill_requests = RefillRequest.objects.filter(patient=request.user).order_by(
        "-requested_at"
    )
    
    # Get IDs of medications with pending requests (to disable button in template)
    pending_med_ids = set(
        RefillRequest.objects.filter(
            patient=request.user,
            status=RefillRequest.Status.PENDING,
        ).values_list("medication_id", flat=True)
    )
    
    return render(
        request,
        "accounts/patient_dashboard.html",
        {
            "medications": medications,
            "refill_requests": refill_requests,
            "pending_med_ids": pending_med_ids,
        },
    )


@login_required
def login_redirect(request):
    """Redirect users to the correct dashboard based on role."""
    # Superusers go to Django admin
    if request.user.is_superuser:
        return redirect("admin:index")
    
    profile = getattr(request.user, "profile", None)
    if profile is None:
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={"role": Profile.Role.PATIENT},
        )
    
    if profile.role == Profile.Role.PROVIDER:
        return redirect("provider-dashboard")
    if profile.role == Profile.Role.STAFF:
        return redirect("staff-dashboard")
    return redirect("patient-dashboard")


def _ensure_staff(user):
    """Check if user has STAFF role."""
    profile = getattr(user, "profile", None)
    return profile and profile.role == Profile.Role.STAFF


@login_required
def staff_dashboard(request):
    """Dashboard for clinic staff to manage patients and view statistics."""
    if not _ensure_staff(request.user):
        return HttpResponseForbidden("Only staff can view this page.")
    
    # System statistics
    total_patients = Profile.objects.filter(role=Profile.Role.PATIENT).count()
    total_providers = Profile.objects.filter(role=Profile.Role.PROVIDER).count()
    pending_refills = RefillRequest.objects.filter(
        status=RefillRequest.Status.PENDING
    ).count()
    total_medications = Medication.objects.count()
    
    # Recent activity
    recent_requests = RefillRequest.objects.order_by("-requested_at")[:10]
    
    return render(
        request,
        "accounts/staff_dashboard.html",
        {
            "total_patients": total_patients,
            "total_providers": total_providers,
            "pending_refills": pending_refills,
            "total_medications": total_medications,
            "recent_requests": recent_requests,
        },
    )


@login_required
def staff_create_patient(request):
    """Allow staff to create new patient accounts."""
    if not _ensure_staff(request.user):
        return HttpResponseForbidden("Only staff can view this page.")
    
    error = None
    success = None
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        
        if not username or not password:
            error = "Username and password are required."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                # Profile auto-created with PATIENT role via signal
                success = f"Patient '{username}' created successfully."
            except Exception as exc:
                error = "Failed to create user. Please try again."
    
    return render(
        request,
        "accounts/staff_create_patient.html",
        {"error": error, "success": success},
    )


@login_required
def staff_add_medication(request):
    """Allow staff to add medications to patient records."""
    if not _ensure_staff(request.user):
        return HttpResponseForbidden("Only staff can view this page.")
    
    patients = User.objects.filter(profile__role=Profile.Role.PATIENT).order_by("username")
    error = None
    success = None
    
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        name = request.POST.get("name", "").strip()
        dose = request.POST.get("dose", "").strip()
        frequency = request.POST.get("frequency", "").strip()
        
        if not all([patient_id, name, dose, frequency]):
            error = "All fields are required."
        else:
            try:
                patient = User.objects.get(id=int(patient_id), profile__role=Profile.Role.PATIENT)
                Medication.objects.create(
                    patient=patient,
                    name=name,
                    dose=dose,
                    frequency=frequency,
                )
                success = f"Medication '{name}' added for {patient.username}."
            except (User.DoesNotExist, ValueError):
                error = "Invalid patient selected."
    
    return render(
        request,
        "accounts/staff_add_medication.html",
        {"patients": patients, "error": error, "success": success},
    )
