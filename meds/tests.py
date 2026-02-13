"""
Medications Tests Module

Purpose: Tests for Medication model creation and behavior.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from meds.models import Medication

User = get_user_model()


class MedicationModelTests(TestCase):
    """Tests for the Medication model."""

    def setUp(self):
        """Set up test data."""
        self.patient = User.objects.create_user(username="patient", password="test123")

    def test_medication_creation(self):
        """Medication can be created with required fields."""
        med = Medication.objects.create(
            patient=self.patient,
            name="Lisinopril",
            dose="10mg",
            frequency="once daily"
        )
        self.assertEqual(med.name, "Lisinopril")
        self.assertEqual(med.patient, self.patient)
        self.assertTrue(med.active)
