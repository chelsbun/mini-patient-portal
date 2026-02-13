from django.urls import path

from .views import approve_refill, cancel_refill, deny_refill, provider_dashboard, request_refill

urlpatterns = [
    path("request/<int:medication_id>/", request_refill, name="request-refill"),
    path("cancel/<int:refill_request_id>/", cancel_refill, name="cancel-refill"),
    path("provider/", provider_dashboard, name="provider-dashboard"),
    path("approve/<int:refill_request_id>/", approve_refill, name="approve-refill"),
    path("deny/<int:refill_request_id>/", deny_refill, name="deny-refill"),
]
