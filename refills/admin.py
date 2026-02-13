from django.contrib import admin

from refills.models import RefillRequest


@admin.register(RefillRequest)
class RefillRequestAdmin(admin.ModelAdmin):
    list_display = ("medication", "patient", "status", "requested_at", "reviewed_at", "reviewed_by")
    list_filter = ("status",)
    search_fields = ("medication__name", "patient__username")
    readonly_fields = ("requested_at",)
