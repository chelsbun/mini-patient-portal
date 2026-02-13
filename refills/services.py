"""
Refills Services Module

Purpose: Business logic for refill request workflow (approve, deny, cancel operations).
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.db import transaction
from django.utils import timezone

from accounts.models import Profile
from refills.models import RefillRequest


class InvalidTransitionError(Exception):
    """Raised when a refill request status transition is not allowed."""
    pass


def _ensure_provider(user):
    """
    Verify that user has PROVIDER role.
    
    Args:
        user: Django User instance to check
        
    Raises:
        PermissionError: If user is not a provider
    """
    if not hasattr(user, "profile") or user.profile.role != Profile.Role.PROVIDER:
        raise PermissionError("Only providers can review refill requests.")


@transaction.atomic
def approve_request(refill_request, provider, note=""):
    """Approve a pending refill request. Only providers can approve."""
    _ensure_provider(provider)

    if refill_request.status != RefillRequest.Status.PENDING:
        raise InvalidTransitionError("Only PENDING requests can be approved.")

    refill_request.status = RefillRequest.Status.APPROVED
    refill_request.reviewed_by = provider
    refill_request.reviewed_at = timezone.now()
    refill_request.provider_note = note
    refill_request.save()
    return refill_request


@transaction.atomic
def deny_request(refill_request, provider, note=""):
    """Deny a pending refill request. Only providers can deny."""
    _ensure_provider(provider)

    if refill_request.status != RefillRequest.Status.PENDING:
        raise InvalidTransitionError("Only PENDING requests can be denied.")

    refill_request.status = RefillRequest.Status.DENIED
    refill_request.reviewed_by = provider
    refill_request.reviewed_at = timezone.now()
    refill_request.provider_note = note
    refill_request.save()
    return refill_request


@transaction.atomic
def cancel_request(refill_request, patient):
    """Cancel a pending refill request. Only the owning patient can cancel."""
    if refill_request.patient != patient:
        raise PermissionError("You can only cancel your own requests.")

    if refill_request.status != RefillRequest.Status.PENDING:
        raise InvalidTransitionError("Only PENDING requests can be cancelled.")

    refill_request.status = RefillRequest.Status.CANCELLED
    refill_request.save()
    return refill_request
