"""
Refills Views Module

Purpose: Handles refill request creation, provider dashboard, and approve/deny/cancel actions.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.http import require_POST

from accounts.models import Profile
from meds.models import Medication
from refills.models import RefillRequest
from refills.services import InvalidTransitionError, approve_request, deny_request, cancel_request


@login_required
@require_POST
def request_refill(request, medication_id):
    """
    Create a new refill request for a patient's medication.
    
    Args:
        request: HTTP request object
        medication_id: ID of the medication to refill
        
    Returns:
        Redirect to patient dashboard on success, or 400 if duplicate pending request exists.
    """
    medication = get_object_or_404(
        Medication,
        id=medication_id,
        patient=request.user,
    )
    
    # Prevent duplicate pending requests for same medication
    existing_pending = RefillRequest.objects.filter(
        medication=medication,
        patient=request.user,
        status=RefillRequest.Status.PENDING,
    ).exists()
    
    if existing_pending:
        return HttpResponseBadRequest("A pending refill request already exists for this medication.")
    
    RefillRequest.objects.create(
        medication=medication,
        patient=request.user,
    )
    return redirect("patient-dashboard")


@login_required
def provider_dashboard(request):
    """
    Display the provider dashboard with pending refill requests and recent history.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered provider dashboard template, or 403 if user is not a provider.
    """
    if not hasattr(request.user, "profile") or request.user.profile.role != Profile.Role.PROVIDER:
        return HttpResponseForbidden("Only providers can view this page.")

    pending_requests = RefillRequest.objects.filter(
        status=RefillRequest.Status.PENDING
    ).order_by("-requested_at")
    
    processed_requests = RefillRequest.objects.filter(
        reviewed_by=request.user
    ).exclude(
        status=RefillRequest.Status.PENDING
    ).order_by("-reviewed_at")[:10]
    
    return render(
        request,
        "refills/provider_dashboard.html",
        {
            "pending_requests": pending_requests,
            "processed_requests": processed_requests,
        },
    )


@login_required
@require_POST
def approve_refill(request, refill_request_id):
    """
    Approve a pending refill request (provider only).
    
    Args:
        request: HTTP request object with optional 'note' in POST data
        refill_request_id: ID of the refill request to approve
        
    Returns:
        Redirect to provider dashboard on success, or 400 on permission/transition error.
    """
    refill_request = get_object_or_404(RefillRequest, id=refill_request_id)
    note = request.POST.get("note", "")
    try:
        approve_request(refill_request, request.user, note=note)
    except PermissionError as exc:
        return HttpResponseForbidden(str(exc))
    except InvalidTransitionError as exc:
        return HttpResponseBadRequest(str(exc))
    return redirect("provider-dashboard")


@login_required
@require_POST
def deny_refill(request, refill_request_id):
    """
    Deny a pending refill request (provider only).
    
    Args:
        request: HTTP request object with optional 'note' in POST data
        refill_request_id: ID of the refill request to deny
        
    Returns:
        Redirect to provider dashboard on success, or 400 on permission/transition error.
    """
    refill_request = get_object_or_404(RefillRequest, id=refill_request_id)
    note = request.POST.get("note", "")
    try:
        deny_request(refill_request, request.user, note=note)
    except PermissionError as exc:
        return HttpResponseForbidden(str(exc))
    except InvalidTransitionError as exc:
        return HttpResponseBadRequest(str(exc))
    return redirect("provider-dashboard")


@login_required
@require_POST
def cancel_refill(request, refill_request_id):
    """
    Cancel a pending refill request (patient only, own requests).
    
    Args:
        request: HTTP request object
        refill_request_id: ID of the refill request to cancel
        
    Returns:
        Redirect to patient dashboard on success, or 400 on permission/transition error.
    """
    refill_request = get_object_or_404(RefillRequest, id=refill_request_id)
    try:
        cancel_request(refill_request, request.user)
    except PermissionError as exc:
        return HttpResponseForbidden(str(exc))
    except InvalidTransitionError as exc:
        return HttpResponseBadRequest(str(exc))
    return redirect("patient-dashboard")
