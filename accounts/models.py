from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        PROVIDER = "PROVIDER", "Provider"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"
