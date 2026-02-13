"""
Accounts Tests Module

Purpose: Tests for Profile model creation and role-based login redirects.
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()


class ProfileCreationTests(TestCase):
    def test_profile_created_on_user_creation(self):
        """Profile is auto-created when a user is created."""
        user = User.objects.create_user(username="newuser", password="test123")
        
        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(user.profile.role, Profile.Role.PATIENT)

    def test_default_role_is_patient(self):
        """New users default to patient role."""
        user = User.objects.create_user(username="testuser", password="test123")
        
        self.assertEqual(user.profile.role, Profile.Role.PATIENT)

    def test_profile_model_default_role(self):
        """Profile created directly without role defaults to PATIENT."""
        user = User.objects.create_user(username="directuser", password="test123")
        user.profile.delete()  # Remove auto-created profile
        
        # Create profile without specifying role
        profile = Profile.objects.create(user=user)
        self.assertEqual(profile.role, Profile.Role.PATIENT)


class LoginRedirectTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.patient = User.objects.create_user(username="patient", password="test123")
        self.patient.profile.role = Profile.Role.PATIENT
        self.patient.profile.save()
        
        self.provider = User.objects.create_user(username="provider", password="test123")
        self.provider.profile.role = Profile.Role.PROVIDER
        self.provider.profile.save()

    def test_patient_redirected_to_patient_dashboard(self):
        """Patients are redirected to patient dashboard."""
        self.client.login(username="patient", password="test123")
        response = self.client.get("/portal/")
        
        self.assertRedirects(response, "/dashboard/")

    def test_provider_redirected_to_provider_dashboard(self):
        """Providers are redirected to provider dashboard."""
        self.client.login(username="provider", password="test123")
        response = self.client.get("/portal/")
        
        self.assertRedirects(response, "/refills/provider/")

    def test_staff_redirected_from_patient_dashboard(self):
        """Staff accessing patient dashboard are redirected to staff dashboard."""
        staff = User.objects.create_user(username="staff", password="test123")
        staff.profile.role = Profile.Role.STAFF
        staff.profile.save()
        
        self.client.login(username="staff", password="test123")
        response = self.client.get("/dashboard/")
        
        self.assertRedirects(response, "/staff/")
