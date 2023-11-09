from django.urls import path, include

from meters.views import MetersView, MeterDetailsView

urlpatterns = [
    path("", MetersView.as_view(), name="meters"),
    path("<int:meter_id>", MeterDetailsView.as_view(), name="meter_details"),
    path("<int:meter_id>/readings/", include("readings.urls")),
    path("<int:meter_id>/tariffs/", include("tariffs.urls")),
]
