from django.urls import path

from tariffs.views import TariffsView, TariffDetailsView

urlpatterns = [
    path("", TariffsView.as_view(), name="tariffs"),
    path("<int:tariff_id>", TariffDetailsView.as_view(), name="tariff_details"),
]
