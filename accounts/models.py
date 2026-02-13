"""
Accounts Models Module

Purpose: Defines user Profile model with role-based access control (PATIENT, PROVIDER, STAFF).
Author: Chelsea Bonyata
Last Modified: February 2026
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Stores a user's role for portal access control."""
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        PROVIDER = "PROVIDER", "Provider"
        STAFF = "STAFF", "Staff"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """Auto-create a patient profile when a new user is registered."""
    if created:
        Profile.objects.get_or_create(
            user=instance,
            defaults={"role": Profile.Role.PATIENT},
        )
