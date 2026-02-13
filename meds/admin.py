from django.contrib import admin

from meds.models import Medication


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ("name", "patient", "dose", "frequency", "active")
    list_filter = ("active",)
