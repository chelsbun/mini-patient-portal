"""
Refills Tests Module

Purpose: Tests for refill request workflow including approve, deny, cancel, and duplicate prevention.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from accounts.models import Profile
from meds.models import Medication
from refills.models import RefillRequest
from refills.services import approve_request, deny_request, cancel_request, InvalidTransitionError

User = get_user_model()


class RefillServiceTests(TestCase):
    def setUp(self):
        # Create a patient user
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.patient.profile.role = Profile.Role.PATIENT
        self.patient.profile.save()
        
        # Create a provider user
        self.provider = User.objects.create_user(username="provider", password="test123")
        self.provider.profile.role = Profile.Role.PROVIDER
        self.provider.profile.save()
        
        # Create a medication for the patient
        self.medication = Medication.objects.create(
            patient=self.patient,
            name="Lisinopril",
            dose="10mg",
            frequency="Once daily"
        )
        
        # Create a pending refill request
        self.refill = RefillRequest.objects.create(
            medication=self.medication,
            patient=self.patient
        )

    def test_approve_request_success(self):
        """Provider can approve a pending request."""
        result = approve_request(self.refill, self.provider, note="Approved")
        
        self.assertEqual(result.status, RefillRequest.Status.APPROVED)
        self.assertEqual(result.reviewed_by, self.provider)
        self.assertEqual(result.provider_note, "Approved")
        self.assertIsNotNone(result.reviewed_at)

    def test_deny_request_success(self):
        """Provider can deny a pending request."""
        result = deny_request(self.refill, self.provider, note="Need appointment first")
        
        self.assertEqual(result.status, RefillRequest.Status.DENIED)
        self.assertEqual(result.reviewed_by, self.provider)
        self.assertEqual(result.provider_note, "Need appointment first")

    def test_patient_cannot_approve(self):
        """Patients cannot approve refill requests."""
        with self.assertRaises(PermissionError):
            approve_request(self.refill, self.patient)

    def test_patient_cannot_deny(self):
        """Patients cannot deny refill requests."""
        with self.assertRaises(PermissionError):
            deny_request(self.refill, self.patient)

    def test_cannot_approve_already_approved(self):
        """Cannot approve a request that's already approved."""
        approve_request(self.refill, self.provider)
        
        with self.assertRaises(InvalidTransitionError):
            approve_request(self.refill, self.provider)

    def test_cannot_deny_already_denied(self):
        """Cannot deny a request that's already denied."""
        deny_request(self.refill, self.provider)
        
        with self.assertRaises(InvalidTransitionError):
            deny_request(self.refill, self.provider)

    def test_cancel_request_success(self):
        """Patient can cancel their own pending request."""
        result = cancel_request(self.refill, self.patient)
        
        self.assertEqual(result.status, RefillRequest.Status.CANCELLED)

    def test_cannot_cancel_other_patients_request(self):
        """Patient cannot cancel another patient's request."""
        other_patient = User.objects.create_user(username="other", password="test123")
        
        with self.assertRaises(PermissionError):
            cancel_request(self.refill, other_patient)

    def test_cannot_cancel_approved_request(self):
        """Cannot cancel a request that's already approved."""
        approve_request(self.refill, self.provider)
        
        with self.assertRaises(InvalidTransitionError):
            cancel_request(self.refill, self.patient)

    def test_cannot_approve_cancelled_request(self):
        """Cannot approve a request that's been cancelled."""
        cancel_request(self.refill, self.patient)
        
        with self.assertRaises(InvalidTransitionError):
            approve_request(self.refill, self.provider)

    def test_cannot_deny_cancelled_request(self):
        """Cannot deny a request that's been cancelled."""
        cancel_request(self.refill, self.patient)
        
        with self.assertRaises(InvalidTransitionError):
            deny_request(self.refill, self.provider)


class DuplicateRequestTests(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.patient.profile.role = Profile.Role.PATIENT
        self.patient.profile.save()
        
        self.medication = Medication.objects.create(
            patient=self.patient,
            name="Lisinopril",
            dose="10mg",
            frequency="Once daily"
        )

    def test_cannot_create_duplicate_pending_request(self):
        """Cannot request refill when one is already pending for same medication."""
        from django.test import Client
        
        client = Client()
        client.login(username="patient", password="test123")
        
        # First request should succeed
        response = client.post(f"/refills/request/{self.medication.id}/")
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Second request should fail
        response = client.post(f"/refills/request/{self.medication.id}/")
        self.assertEqual(response.status_code, 400)  # Bad request

    def test_can_request_after_previous_approved(self):
        """Can request new refill after previous one was approved."""
        from django.test import Client
        
        client = Client()
        client.login(username="patient", password="test123")
        
        # Create and approve a request
        refill = RefillRequest.objects.create(
            medication=self.medication,
            patient=self.patient
        )
        refill.status = RefillRequest.Status.APPROVED
        refill.save()
        
        # New request should succeed
        response = client.post(f"/refills/request/{self.medication.id}/")
        self.assertEqual(response.status_code, 302)


class RefillViewStatusCodeTests(TestCase):
    """Tests for HTTP status codes returned by refill views."""
    
    def setUp(self):
        """Set up test data for view tests."""
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.patient.profile.role = Profile.Role.PATIENT
        self.patient.profile.save()
        
        self.provider = User.objects.create_user(username="provider", password="test123")
        self.provider.profile.role = Profile.Role.PROVIDER
        self.provider.profile.save()
        
        self.medication = Medication.objects.create(
            patient=self.patient, name="TestMed", dose="10mg", frequency="daily"
        )
        self.refill = RefillRequest.objects.create(
            medication=self.medication, patient=self.patient
        )
        self.client = Client()

    def test_patient_approve_returns_403(self):
        """Patient attempting to approve should get 403 Forbidden."""
        self.client.login(username="patient", password="test123")
        response = self.client.post(f"/refills/approve/{self.refill.id}/")
        self.assertEqual(response.status_code, 403)

    def test_patient_deny_returns_403(self):
        """Patient attempting to deny should get 403 Forbidden."""
        self.client.login(username="patient", password="test123")
        response = self.client.post(f"/refills/deny/{self.refill.id}/")
        self.assertEqual(response.status_code, 403)

    def test_other_patient_cancel_returns_403(self):
        """Patient cancelling another patient's request should get 403."""
        other_patient = User.objects.create_user(username="other", password="test123")
        other_patient.profile.role = Profile.Role.PATIENT
        other_patient.profile.save()
        
        self.client.login(username="other", password="test123")
        response = self.client.post(f"/refills/cancel/{self.refill.id}/")
        self.assertEqual(response.status_code, 403)
