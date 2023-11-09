from django.urls import path

from readings.views import ReadingsView

urlpatterns = [
    path("", ReadingsView.as_view(), name="readings"),
]
