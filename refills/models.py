"""
Refills Models Module

Purpose: Defines RefillRequest model with status workflow (PENDING, APPROVED, DENIED, CANCELLED).
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.conf import settings
from django.db import models


class RefillRequest(models.Model):
    """
    Represents a patient's request to refill a medication.
    
    Tracks status workflow: PENDING -> APPROVED/DENIED/CANCELLED.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        DENIED = "DENIED", "Denied"
        CANCELLED = "CANCELLED", "Cancelled"

    medication = models.ForeignKey(
        "meds.Medication",
        on_delete=models.CASCADE,
        related_name="refill_requests",
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="refill_requests",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_refill_requests",
    )
    provider_note = models.TextField(blank=True)

    def __str__(self):
        return f"RefillRequest({self.medication.name}, {self.status})"
