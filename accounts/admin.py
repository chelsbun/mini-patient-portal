from django.contrib import admin

from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile records."""

    list_display = ("user", "role")
