"""
Medications Models Module

Purpose: Defines Medication model linking prescriptions to patients.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.conf import settings
from django.db import models


class Medication(models.Model):
    """
    Represents a medication prescribed to a patient.
    
    Stores medication name, dosage, frequency, and active status.
    """
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medications",
    )
    name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.dose}) - {self.patient.username}"
