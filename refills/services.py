from django.db import transaction
from django.utils import timezone

from accounts.models import Profile
from refills.models import RefillRequest


class InvalidTransitionError(Exception):
    pass


def _ensure_provider(user):
    if not hasattr(user, "profile") or user.profile.role != Profile.Role.PROVIDER:
        raise PermissionError("Only providers can review refill requests.")


@transaction.atomic
def approve_request(refill_request: RefillRequest, provider, note: str = "") -> RefillRequest:
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
def deny_request(refill_request: RefillRequest, provider, note: str = "") -> RefillRequest:
    _ensure_provider(provider)

    if refill_request.status != RefillRequest.Status.PENDING:
        raise InvalidTransitionError("Only PENDING requests can be denied.")

    refill_request.status = RefillRequest.Status.DENIED
    refill_request.reviewed_by = provider
    refill_request.reviewed_at = timezone.now()
    refill_request.provider_note = note
    refill_request.save()
    return refill_request
